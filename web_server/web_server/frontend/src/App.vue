<template>
  <div class="container">
    <form action="#">
      <div class="input-field inline">
        <input v-model="user_id" id="user_id" placeholder="Enter vk.com profile">
      </div>
      <div class="range-field">
        <input v-model="popularity" type="range" id="pop_lvl" min="1" max="10" />
      </div>
      <button class="waves-effect waves-light btn-small" v-on:click="get_rec_bands()">
        <span>Enjoy</span>
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
.container {
	width: 400px !important;
}

form {
display: flex;
flex-direction: column;
background-color: #fff;
max-width: 320px;
padding: 2rem 2rem 2rem 2rem;
position: relative;
box-shadow: 0 1px 1px rgba(0, 0, 0, 0.20);
}

.container.input-field inline, .range-field{
display: flex;
flex-flow: column-reverse;
margin-bottom: 1em;
}


</style>
