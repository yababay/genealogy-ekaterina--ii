<script lang="ts">
    import { onMount } from "svelte"
    import { Network, parseDOTNetwork } from "vis-network/standalone/umd/vis-network.min"
    import { options, dotFiles, links } from './settints.json'

    let container: HTMLElement

    async function loadSingle(fn){
        const res = await fetch(`${fn}.dot`)
        if(!res.ok) throw new Error("Не удалось загрузить сведения о генеологии.")
        return (await res.text())
    }

    onMount(async () => {
        const lines = await Promise.all(dotFiles.map(loadSingle))
            .then(arr => arr.join('\n'))        
        const data = parseDOTNetwork(lines)
        const network = new Network(container, data, options)
        network.on("click", ctx => {
            const { nodes } = ctx
            if(!nodes || nodes.length != 1) return
            const [ node ] = nodes
            const link = links[node]
            if(!link) return
            window.open(link, "_blank")

        })

        network.on("hoverNode", function (params) {
           network.canvas.body.container.style.cursor = 'pointer';
        });

        network.on("blurNode", function (params) {
            network.canvas.body.container.style.cursor = 'default';
        });
    })
</script>

<div bind:this={container} class="genealogy-holder"></div>

<style>
    .genealogy-holder {
        width: 100%;
        min-height: 100% !important;
    }
</style>
