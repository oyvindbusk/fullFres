<template>
  <div>
    {{ loggedInStatus }}
    <h1>All samples</h1>
    <br>
    <div class="container" id="login">
      <div class="row row justify-content-center">
        <div class="col-md-10">
          <b-table
            selectable
            select-mode="single"
            @row-selected="rowSelected"
            striped
            hover
            outlined
            :items="items"
            :fields="fields"
            :small="small"
          >
          <!-- Formatting Type column -->
          <template #cell(runid)="data">
            <b class="text-info">{{ data.value.toUpperCase() }}</b>
          </template>
          </b-table>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { config } from "../config.js";
import axios from "axios";
//import util_funcs from "@/appUtils";

export default {
  name: "varianttable",
  data() {
    return {
      loggedInStatus: false,
      small: true,
      sampleID: "",
      selectedSample: "",
      items: [],
      fields: [{key: "runid", label: "Run id"}, 
              {key: "sampleid", label: "Sample id"},
              {key: "Date_Signoff", label: "Date Sign off"},
              {key: "Date_Approval", label: "Date Approval"}],
    };
  },
  methods: {
    rowSelected(items) {
      if (items.length === 1) {
        this.selectedSample = items[0].sampleid;
      } else if (items.length === 0) {
        this.selectedSample = "";
      }
    },
    getsamples() {
      // Funksjon for å få samples fra backenc
      // util_funcs.query_backend(config.$backend_url,'samples').then(result => this.items = JSON.parse(result['data']))
      console.log("metode testaxios");
      const baseURI = config.$backend_url + "/api/allsamples";
      axios
        .get(baseURI)
        .then((response) => response.data)
        .then((data) => (this.items = data.data));
    },
  },
  created: function () {
    // initstore sjekk innlogging
    this.$store.dispatch("initStore");
    this.getsamples();
  },
  watch: {
    state(newState, oldState) {
      console.log(`State changed from ${oldState} to ${newState}`);
    },
    selectedSample: function () {
      this.$router.push({
        name: "Variants",
        params: { id: this.selectedSample },
      });
    },
  },
  computed: {
    state() {
      return this.$store.getters.loggedInStatus;
    },
  },
};
</script>
