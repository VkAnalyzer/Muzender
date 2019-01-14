<template>
  <div class="container">
    <div class="page-loader" v-if="loading">
      <div class="lds-facebook"><div></div><div></div><div></div></div>
    </div>
    <form action="#">
      <div class="input-field inline">
        <input v-model="user_id" id="user_id" placeholder="Enter vk.com profile">
      </div>
      <p id="vk-id-example">Example: https://vk.com/id42</p>
      <div class="range-field">
        <input v-model="popularity" type="range" id="pop_lvl" min="1" max="10">
      </div>
      <p id="popularity-description">Group popularity.
        Select "1" in order to get the most unexpected recommendations</p>
      <button class="waves-effect waves-light btn-small" v-on:click="get_rec_bands()">
        <span>Listen</span>
      </button>
      </div>
    </form>

    <p v-show="rec_bands">We recommend you to listen the following bands:</p>
      <ul>
        <li v-for="band in rec_bands">
          {{ band }}
        </li>
      </ul>
  </div>
</template>

<script>
import {MuzenderAPI} from './API/MuzenderAPI'

const muzender_api = new MuzenderAPI()

export default {
  name: 'app',
  data() {
    return {
      rec_bands: '',
      user_id: '',
      popularity: 6,
      loading: false
    };
  },
  mounted() {
      this.$nextTick(function () {
        var array_of_dom_elements = document.querySelectorAll("input[type=range]");
        M.Range.init(array_of_dom_elements);
      });
  },
  methods: {
    get_rec_bands() {
      let user = {user_id: this.user_id,
                  popularity_level: this.popularity}
      this.loading = true
      muzender_api.get_rec_bands(user).then((response_data) => {
        this.rec_bands = response_data
        this.loading = false
      })
    }
  }
}
</script>

<style>
.container {
	width: 400px !important;
}

form {
  display: flex;
  flex-direction: column;
  margin: auto;
  max-width: 320px;
  padding: 3rem;
  position: relative;
  background: #474A59;
  box-shadow: 0px 0px 40px 16px rgba(0,0,0,0.22);
  color: #F1F1F2;
}

.container .input-field.inline, .range-field {
  display: flex;
  flex-flow: column-reverse;
  margin: 1em 0em 0em 0em;
  margin-bottom: 0rem !important;
}

#vk-id-example, #popularity-description {
  margin: 0em 0em 1.5em 0em;
  font-size: 0.75rem;
  font-style: italic;
}

input[type=range] {
  border: 0px !important;
}

input[type=range]+.thumb.active .value {
  color: #474A59 !important;
}

.container .waves-effect.waves-light.btn-small {
  margin: 2em 4em 0em 4em;
  border-radius: 0px;
  /*
  position: absolute;
  width: 50%;
  right: 25%;
  bottom: -20px;
  */
}

#user_id {
  color: #f2f2f2;
}

.page-loader {
  position: absolute;
  top: 0;
  bottom: 0%;
  left: 0;
  right: 0%;
  background-color: rgba(0,0,0,0.8);
  z-index: 99;
  display: block;
  text-align: center;
  width: 100%;
}

.lds-facebook {
  position: fixed;
  z-index: 999;
  overflow: visible;
  margin: auto;
  top: 0;
  left: 0;
  bottom: 0;
  right: 0;
  width: 64px;
  height: 64px;
}
.lds-facebook div {
  display: inline-block;
  position: absolute;
  left: 6px;
  width: 13px;
  background: #26a69a;
  animation: lds-facebook 1.2s cubic-bezier(0, 0.5, 0.5, 1) infinite;
}
.lds-facebook div:nth-child(1) {
  left: 6px;
  animation-delay: -0.24s;
}
.lds-facebook div:nth-child(2) {
  left: 26px;
  animation-delay: -0.12s;
}
.lds-facebook div:nth-child(3) {
  left: 45px;
  animation-delay: 0;
}
@keyframes lds-facebook {
  0% {
    top: 6px;
    height: 51px;
  }
  50%, 100% {
    top: 19px;
    height: 26px;
  }
}


</style>
