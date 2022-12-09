<script lang="ts">
    import { onMount } from "svelte"
    import { Network, parseDOTNetwork } from "vis-network/standalone/umd/vis-network.min"
    let container: HTMLElement

    onMount(async () => {
        const res = await fetch("index.dot")
        if(!res.ok) throw new Error("Не удалось загрузить сведения о генеологии.")
        const text = await res.text()
        const data = parseDOTNetwork(text)
        const options = {
            locale: 'ru',
            layout: {
                hierarchical: {
                    enabled: true,
                    sortMethod: 'directed',
                }
            },
            groups: {
                "Ростислав": {
                    color: {background:'lightblue'}
                },
                "Мстислав": {
                    color: {background:'lightseagreen'}
                },
                "Софья": {
                    color: {background:'lemonchiffon'}
                },
                "Вальдемар": {
                    color: {background:'lavenderblush'}
                },
                "Эрик X": {
                    color: {background:'lightseagreen'}
                },
                "Евдокия Мешко": {
                    color: {background:'lightcoral'}
                },
                "Кристофер I": {
                    color: {background:'lightgrey'}
                }
            }
        }
        Reflect.construct(Network, [container, data, options])
        const canvas = container.querySelector('canvas')
        //canvas.setAttribute('height', `${container.offsetHeight}`)
    })
</script>

<div bind:this={container} class="genealogy-holder"></div>

<style>
    .genealogy-holder {
        width: 100%;
        min-height: 100% !important;
    }
</style>
