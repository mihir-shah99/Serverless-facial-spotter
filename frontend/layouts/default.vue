<template>
  <v-app dark>
   
    <v-app-bar app height="100">
      <v-avatar class="mr-3 mx-12"  size="70">
        <v-img contain max-height="70%"
          src="https://picsum.photos/200"
        ></v-img>
      </v-avatar>

      <v-toolbar-title class=" display-2 .font-italic  blue--text text--{darken}-1 mx-auto">
       Serverless Facial Spotter 
      </v-toolbar-title>
    <div class="mx-12">
        <v-btn large  v-if="$auth.loggedIn" @click="$auth.logout()" color="primary">Sign off</v-btn>  
        <v-btn large  v-else @click="$auth.loginWith('auth0')" color="primary">Login</v-btn>  
    </div>
    </v-app-bar>
        <v-content>
            <v-container>
              <nuxt />
            </v-container>
        </v-content>
  </v-app>
</template>

<script>
import { mapGetters } from 'vuex'

export default {


  data () {
    return {
      clipped: false,
      drawer: false,
      fixed: false,
      items: [
        {
          icon: 'mdi-apps',
          title: 'Welcome',
          to: '/'
        },
        {
          icon: 'mdi-chart-bubble',
          title: 'Inspire',
          to: '/inspire'
        }
      ],
      miniVariant: false,
      right: true,
      rightDrawer: false,
      title: 'Vuetify.js'
    }
  },
  computed: mapGetters(['isAuthenticated'])

}
</script>
