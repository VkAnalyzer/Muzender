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
        <input v-model.number="popularity" type="range" id="pop_lvl" min="1" max="10">
      </div>
      <p id="popularity-description">Band popularity.
        Select "1" in order to get the most unexpected recommendations</p>
      <button class="waves-effect waves-light btn-small" v-on:click="get_rec_bands()">
        <span>Listen</span>
      </button>
    </form>
    <transition name="slide-fade">
      <div class="recs" v-if="rec_bands">
        <h5>Enjoy the following bands:</h5>
        <div class="collection">
          <a v-for="band in rec_bands" class="collection-item"
          v-bind:href="'https://music.yandex.ru/search?text='+band.trim().replace(' ', '%20')+'&type=artists'"
          target="_blank">
            {{ band.charAt(0).toUpperCase() + band.slice(1) }}
          </a>
        </div>
      </div>
    </transition>
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
        this.loading = false
        if (response_data.length > 5) { // length of recommendations
          M.toast({html: response_data})
        } else {
          this.rec_bands = response_data
        }
      })
    }
  }
}
</script>

<style>
.container {
  display: flex;
  height: 320px;
  margin: 0 auto;
	width: 640px !important;
}

form {
  display: flex;
  flex-direction: column;
  margin: auto;
  width: 50%;
  height: 100%;
  padding: 2rem 3rem 1.5rem 3rem;
  position: relative;
  background: #474A59;
  box-shadow: 0px 0px 40px 16px rgba(0,0,0,0.22);
  color: #F1F1F2;
  z-index:9
}

.recs {
  background: white;
  height: calc(100% - 40px);
  top: 20px;
  position: relative;
  width: 50%;
 }

.recs .collection {
  border: 0;
  border-radius: 0;
  font-weight: bold;
}

.collection a.collection-item {
  color: #8c8c8c !important;
  text-overflow: ellipsis;
  overflow:hidden;
  white-space:nowrap;
}

.recs h5 {
  color: black;
  text-align: center;
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
  margin: 1.5em 4em 0em 4em;
  /*
  border-radius: 0px;
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

.slide-fade-enter-active {
  transition: all 1.0s ease;
}

.slide-fade-enter {
  transform: translateX(10px);
  opacity: 0;
}

/* Change autofill color */
input:-webkit-autofill,
input:-webkit-autofill:hover,
input:-webkit-autofill:focus,
input:-webkit-autofill:active  {
    -webkit-box-shadow: 0 0 0 30px #474A59 inset !important;
}

input:-webkit-autofill {
    -webkit-text-fill-color: #f2f2f2 !important;
}

</style>
