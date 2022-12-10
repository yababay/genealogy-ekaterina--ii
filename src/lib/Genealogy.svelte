<script lang="ts">
    import { onMount } from "svelte"
    import { Network, parseDOTNetwork } from "vis-network/standalone/umd/vis-network.min"
    import { options, dotFiles, persons } from './settings.json'

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
        data.nodes.forEach(node => {
            const {id} = node
            const person = persons[id]
            const { weight } = person
            const size = weight < 500 && 8 || weight < 1000 && 12 || weight < 5000 && 16 || weight < 10000 && 20 || weight < 50 && 24 || 28
            node.font = {size}
        });
        const network = new Network(container, data, options)
        network.on("click", ctx => {
            const { nodes } = ctx
            if(!nodes || nodes.length != 1){
                // TODO: network.canvas.body.container.style.cursor = 'grabbing'
                return
            }
            const [ node ] = nodes
            const person = persons[node]
            if(!person || !person.link) return
            window.open(person.link, "_blank")
        })

        network.on("hoverNode", function (params) {
           network.canvas.body.container.style.cursor = 'pointer'
        });

        network.on("blurNode", function (params) {
            network.canvas.body.container.style.cursor = 'grabbing'
        });

        network.focus('MS', {scale: 1})
        network.canvas.body.container.style.cursor = 'grabbing'
    })
</script>

<div bind:this={container} class="genealogy-holder"></div>

<style>
    .genealogy-holder {
        width: 100%;
        min-height: 100% !important;
    }
</style>
