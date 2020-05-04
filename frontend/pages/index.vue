<template>
 <div class="my-12">
 <v-parallax dark src="https://cdn.vuetifyjs.com/images/backgrounds/vbanner.jpg">
    <v-row align="center" justify="center">
      <v-col class="text-center" cols="12">
        <h1 class="display-1 font-weight-thin mb-4">Find yourself now!</h1>
      </v-col>
    </v-row>
  </v-parallax>
  <v-file-input class="my-12" label="Upload your photo" filled prepend-icon="mdi-camera"></v-file-input>

    <userimage></userimage> 
        
        
      <div class="my-12 mx-12">
        <v-btn color="green" block>Find me</v-btn>
      </div>

<v-divider class="my-5"></v-divider>
  <v-card height="150">
    <v-footer
      absolute
      class="font-weight-medium"
    >
      <v-col
        class="text-center"
        cols="12"
      >
        {{ new Date().getFullYear() }} — <strong>Vuetify</strong>
      </v-col>
    </v-footer>
  </v-card>      
 </div>
</template>

<script>
import userimage from '~/components/userimage.vue';
export default {
  components: {
    userimage: userimage,
  }
}
</script>
