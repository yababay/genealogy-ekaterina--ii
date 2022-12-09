import './assets/tailwind.css'
import './assets/hmf.css'
import './assets/index.css'
import App from './App.svelte'

const target = document.querySelector('main')

Reflect.construct(App, [{target}])

export default null
