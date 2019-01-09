<template>
  <div class="input-container">
    <form action="#">
      <input v-model="user_id" id="user_id" placeholder="Enter vk.com profile">
      <p class="range-field">
        <input v-model="popularity" type="range" id="pop_lvl" min="1" max="10" />
      </p>
    </form>
      <button v-on:click="get_rec_bands()">
        <span>Recommend me some cool music</span>
      </button>
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
      let user = {user_id: this.user_id}
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
.input-container {
	width: 400px;
	display: flex;
	flex-direction: column;
	background: transparent;
	max-width: 320px;
	padding: 2rem 2rem 2rem 2rem;
	position: relative;
}
</style>
