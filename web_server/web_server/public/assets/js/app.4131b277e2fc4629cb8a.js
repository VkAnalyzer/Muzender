webpackJsonp([1],{"1uuo":function(e,t){},NHnr:function(e,t,n){"use strict";Object.defineProperty(t,"__esModule",{value:!0});var r=n("7+uW"),a=n("Zrlr"),s=n.n(a),o=n("wxAW"),u=n.n(o),i=n("mtWM"),l=n.n(i),_=new(function(){function e(){s()(this,e)}return u()(e,[{key:"get_rec_bands",value:function(e){return l.a.post("http://localhost:8000/get_rec_bands/",e).then(function(e){return e.data})}}]),e}()),c={name:"app",data:{rec_bands:"sdsds",user_id:"",loading:!1},methods:{get_rec_bands:function(){var e=this;console.log(5);var t={user_id:this.user_id};this.loading=!0,_.get_rec_bands(t).then(function(t){e.rec_bands=t.data,e.loading=!1})}}},v={render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",[e._v("\n  "+e._s(e.rec_bands)+"\n  "),n("input",{directives:[{name:"model",rawName:"v-model",value:e.user_id,expression:"user_id"}],attrs:{placeholder:"Enter vk.com profile"},domProps:{value:e.user_id},on:{input:function(t){t.target.composing||(e.user_id=t.target.value)}}}),e._v(" "),n("button",{on:{click:function(t){e.get_rec_bands()}}},[n("span",[e._v("Recommend me some cool music")])]),e._v(" "),n("p",{directives:[{name:"show",rawName:"v-show",value:e.rec_bands,expression:"rec_bands"}]},[e._v("We recommend you to listen the following bands:")]),e._v(" "),n("ul",e._l(e.rec_bands,function(t){return n("li",[e._v("\n        { band }\n      ")])}))])},staticRenderFns:[]},d=n("VU/8")(c,v,!1,null,null,null).exports,h=n("/ocq"),p={render:function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("div",{staticClass:"hello"},[n("h1",[e._v(e._s(e.msg))]),e._v(" "),n("h2",[e._v("Essential Links")]),e._v(" "),e._m(0),e._v(" "),n("h2",[e._v("Ecosystem")]),e._v(" "),e._m(1)])},staticRenderFns:[function(){var e=this,t=e.$createElement,n=e._self._c||t;return n("ul",[n("li",[n("a",{attrs:{href:"https://vuejs.org",target:"_blank"}},[e._v("\n        Core Docs\n      ")])]),e._v(" "),n("li",[n("a",{attrs:{href:"https://forum.vuejs.org",target:"_blank"}},[e._v("\n        Forum\n      ")])]),e._v(" "),n("li",[n("a",{attrs:{href:"https://chat.vuejs.org",target:"_blank"}},[e._v("\n        Community Chat\n      ")])]),e._v(" "),n("li",[n("a",{attrs:{href:"https://twitter.com/vuejs",target:"_blank"}},[e._v("\n        Twitter\n      ")])]),e._v(" "),n("br"),e._v(" "),n("li",[n("a",{attrs:{href:"http://vuejs-templates.github.io/webpack/",target:"_blank"}},[e._v("\n        Docs for This Template\n      ")])])])},function(){var e=this.$createElement,t=this._self._c||e;return t("ul",[t("li",[t("a",{attrs:{href:"http://router.vuejs.org/",target:"_blank"}},[this._v("\n        vue-router\n      ")])]),this._v(" "),t("li",[t("a",{attrs:{href:"http://vuex.vuejs.org/",target:"_blank"}},[this._v("\n        vuex\n      ")])]),this._v(" "),t("li",[t("a",{attrs:{href:"http://vue-loader.vuejs.org/",target:"_blank"}},[this._v("\n        vue-loader\n      ")])]),this._v(" "),t("li",[t("a",{attrs:{href:"https://github.com/vuejs/awesome-vue",target:"_blank"}},[this._v("\n        awesome-vue\n      ")])])])}]};var m=n("VU/8")({name:"HelloWorld",data:function(){return{msg:"Welcome to Your Vue.js App"}}},p,!1,function(e){n("1uuo")},"data-v-d8ec41bc",null).exports;r.a.use(h.a);var f=new h.a({routes:[{path:"/",name:"HelloWorld",component:m}]});r.a.config.productionTip=!1,new r.a({el:"#app",router:f,components:{App:d},template:"<App/>"})}},["NHnr"]);
//# sourceMappingURL=app.4131b277e2fc4629cb8a.js.map