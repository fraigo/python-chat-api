function imageUrl(url){
    if (url==null || url==""){
        return "images/user-icon.png"
    }
    return url
}

Vue.component("contactselector",{
    props: [
        "imageurl",
        "name",
        "email"
    ],
    template: `<v-layout row>
        <v-avatar class="ma-2" size="32">
            <img :src="imageUrl(imageurl)">
        </v-avatar>
        <div class="ma-2">
            <b>{{ name }}</b>
            <br>
            {{ email }}
        </div>
    </v-layout>`,
    methods:{
        imageUrl: imageUrl,
    }

})

