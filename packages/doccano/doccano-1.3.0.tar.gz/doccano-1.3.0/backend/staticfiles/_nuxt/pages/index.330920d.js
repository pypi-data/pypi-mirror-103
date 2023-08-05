(window.webpackJsonp=window.webpackJsonp||[]).push([[103],{1099:function(t,e,r){"use strict";r.r(e);var n=r(3),o=n.default.extend({props:{title:{type:String,default:"",required:!0},text:{type:String,default:"",required:!0},imageSrc:{type:String,default:"",required:!0}}}),l=r(27),c=r(31),d=r.n(c),h=r(508),f=r(491),v=r(140),component=Object(l.a)(o,(function(){var t=this,e=t.$createElement,r=t._self._c||e;return r("v-card",[r("v-img",{attrs:{src:t.imageSrc,height:"200px"}}),t._v(" "),r("v-card-title",{staticClass:"layout justify-center",attrs:{"primary-title":""}},[r("div",{staticClass:"headline text-xs-center font-weight-bold mb-2"},[t._v("\n      "+t._s(t.title)+"\n    ")])]),t._v(" "),r("v-card-text",{staticClass:"subtitle-1 layout justify-center"},[t._v("\n    "+t._s(t.text)+"\n  ")])],1)}),[],!1,null,null,null),m=component.exports;d()(component,{VCard:h.a,VCardText:f.b,VCardTitle:f.c,VImg:v.a});var _=n.default.extend({components:{FeatureCard:m},data:function(){return{featureCards:[{imageSrc:"feature3.png",title:this.$t("home.featuresTitle1"),text:this.$t("home.featuresText1")},{imageSrc:"feature2.png",title:this.$t("home.featuresTitle2"),text:this.$t("home.featuresText2")},{imageSrc:"feature1.png",title:this.$t("home.featuresTitle3"),text:this.$t("home.featuresText3")}]}}}),x=r(482),y=r(483),k=r(484),w=Object(l.a)(_,(function(){var t=this.$createElement,e=this._self._c||t;return e("v-container",[e("v-layout",{staticClass:"my-5",attrs:{column:"",wrap:"","align-center":""}},[e("v-flex",{staticClass:"my-3",attrs:{xs12:"",sm4:""}},[e("div",{staticClass:"text-xs-center"},[e("h2",{staticClass:"headline"},[this._v("\n          "+this._s(this.$t("home.featuresTitle"))+"\n        ")])])]),this._v(" "),e("v-flex",{attrs:{xs12:""}},[e("v-container",{attrs:{"grid-list-xl":""}},[e("v-layout",{attrs:{wrap:"","align-center":""}},this._l(this.featureCards,(function(t,n){return e("v-flex",{key:n,attrs:{xs12:"",md4:""}},[e("feature-card",{attrs:{"image-src":r(763)("./"+t.imageSrc),title:t.title,text:t.text}})],1)})),1)],1)],1)],1)],1)}),[],!1,null,null,null),O=w.exports;d()(w,{VContainer:x.a,VFlex:y.a,VLayout:k.a});var j=r(195),C=r(170),B=(r(28),r(767),n.default.extend({name:"translatable",props:{height:Number},data:function(){return{elOffsetTop:0,parallax:0,parallaxDist:0,percentScrolled:0,scrollTop:0,windowHeight:0,windowBottom:0}},computed:{imgHeight:function(){return this.objHeight()}},beforeDestroy:function(){window.removeEventListener("scroll",this.translate,!1),window.removeEventListener("resize",this.translate,!1)},methods:{calcDimensions:function(){var t=this.$el.getBoundingClientRect();this.scrollTop=window.pageYOffset,this.parallaxDist=this.imgHeight-this.height,this.elOffsetTop=t.top+this.scrollTop,this.windowHeight=window.innerHeight,this.windowBottom=this.scrollTop+this.windowHeight},listeners:function(){window.addEventListener("scroll",this.translate,!1),window.addEventListener("resize",this.translate,!1)},objHeight:function(){throw new Error("Not implemented !")},translate:function(){this.calcDimensions(),this.percentScrolled=(this.windowBottom-this.elOffsetTop)/(parseInt(this.height)+this.windowHeight),this.parallax=Math.round(this.parallaxDist*this.percentScrolled)}}})),$=r(13),S=Object($.a)(B).extend().extend({name:"v-parallax",props:{alt:{type:String,default:""},height:{type:[String,Number],default:500},src:String,srcset:String},data:function(){return{isBooted:!1}},computed:{styles:function(){return{display:"block",opacity:this.isBooted?1:0,transform:"translate(-50%, ".concat(this.parallax,"px)")}}},mounted:function(){this.init()},methods:{init:function(){var t=this,img=this.$refs.img;img&&(img.complete?(this.translate(),this.listeners()):img.addEventListener("load",(function(){t.translate(),t.listeners()}),!1),this.isBooted=!0)},objHeight:function(){return this.$refs.img.naturalHeight}},render:function(t){var e=t("div",{staticClass:"v-parallax__image-container"},[t("img",{staticClass:"v-parallax__image",style:this.styles,attrs:{src:this.src,srcset:this.srcset,alt:this.alt},ref:"img"})]),content=t("div",{staticClass:"v-parallax__content"},this.$slots.default);return t("div",{staticClass:"v-parallax",style:{height:"".concat(this.height,"px")},on:this.$listeners},[e,content])}}),V=Object(l.a)({},(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("section",[n("v-parallax",{attrs:{src:r(568),height:"400",dark:""}},[n("v-layout",{staticClass:"white--text",attrs:{wrap:"","align-center":"","justify-center":""}},[n("v-flex",{staticClass:"mr-5",attrs:{"text-right":""}},[n("img",{attrs:{src:r(336),alt:"doccano",height:"200"}})]),t._v(" "),n("v-flex",[n("h1",{staticClass:"mb-2 display-1 text-xs-center"},[t._v("\n          "+t._s(t.$t("home.mainTitle"))+"\n        ")]),t._v(" "),n("div",{staticClass:"mt-4"},[n("v-btn",{attrs:{large:"",outlined:"",color:"white",href:"https://github.com/doccano/doccano"}},[n("v-icon",{attrs:{left:""}},[t._v("\n              mdi-github\n            ")]),t._v("\n            GitHub\n          ")],1),t._v(" "),n("v-btn",{staticClass:"blue lighten-2 ml-5",attrs:{dark:"",large:"",href:t.localePath("/auth")}},[t._v("\n            "+t._s(t.$t("home.getStarted"))+"\n          ")])],1)])],1)],1)],1)}),[],!1,null,null,null),z=V.exports;d()(V,{VBtn:j.a,VFlex:y.a,VIcon:C.a,VLayout:k.a,VParallax:S});var T=n.default.extend({data:function(){return{items:[{title:this.$t("home.demoNER"),link:"named-entity-recognition"},{title:this.$t("home.demoSent"),link:"sentiment-analysis"},{title:this.$t("home.demoTranslation"),link:"translation"},{title:this.$t("home.demoTextToSQL"),link:"text-to-sql"}]}}}),E=r(171),P=r(105),D=r(38),L=r(474),H=Object(l.a)(T,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("section",[n("v-parallax",{attrs:{src:r(568),height:"400",dark:""}},[n("v-container",[n("v-layout",{staticClass:"white--text",attrs:{wrap:"","align-center":"","justify-center":""}},[n("v-flex",{attrs:{xs12:"",md7:""}},[n("v-img",{staticClass:"ma-5",attrs:{src:r(605),"max-height":"380",contain:""}})],1),t._v(" "),n("v-flex",{attrs:{xs12:"",md5:""}},[n("h1",{staticClass:"mb-2 display-1 text-xs-center"},[t._v("\n            "+t._s(t.$t("home.footerTitle"))+"\n          ")]),t._v(" "),n("div",{staticClass:"mt-4"},[n("v-menu",{attrs:{"open-on-hover":"","offset-y":""},scopedSlots:t._u([{key:"activator",fn:function(e){var r=e.on;return[n("v-btn",t._g({staticClass:"blue lighten-2",attrs:{dark:"",large:""}},r),[t._v("\n                  "+t._s(t.$t("home.demoDropDown"))+"\n                  "),n("v-icon",[t._v("mdi-menu-down")])],1)]}}])},[t._v(" "),n("v-list",t._l(t.items,(function(e,r){return n("v-list-item",{key:r,on:{click:function(r){t.$router.push(t.localePath("/demo/"+e.link))}}},[n("v-list-item-title",[t._v(t._s(e.title))])],1)})),1)],1)],1)])],1)],1)],1)],1)}),[],!1,null,null,null),N=H.exports;d()(H,{VBtn:j.a,VContainer:x.a,VFlex:y.a,VIcon:C.a,VImg:v.a,VLayout:k.a,VList:E.a,VListItem:P.a,VListItemTitle:D.d,VMenu:L.a,VParallax:S});var F={components:{FeatureCards:O,TheTopBanner:z,TheBottomBanner:N}},I=r(488),M=Object(l.a)(F,(function(){var t=this.$createElement,e=this._self._c||t;return e("v-main",[e("the-top-banner"),this._v(" "),e("feature-cards"),this._v(" "),e("the-bottom-banner")],1)}),[],!1,null,null,null);e.default=M.exports;d()(M,{VMain:I.a})},491:function(t,e,r){"use strict";r.d(e,"a",(function(){return l})),r.d(e,"b",(function(){return d})),r.d(e,"c",(function(){return h}));var n=r(508),o=r(4),l=Object(o.i)("v-card__actions"),c=Object(o.i)("v-card__subtitle"),d=Object(o.i)("v-card__text"),h=Object(o.i)("v-card__title");n.a},507:function(t,e,r){"use strict";r(28);var n=r(3),o=(r(15),r(11),r(9),r(7),r(12),r(115),r(5)),l=(r(521),r(183)),c=r(35),d=r(82),h=r(185),f=r(29),v=r(4),m=r(13);function _(object,t){var e=Object.keys(object);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(object);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(object,t).enumerable}))),e.push.apply(e,r)}return e}var x=Object(m.a)(c.a,Object(d.b)(["absolute","fixed","top","bottom"]),h.a,f.a).extend({name:"v-progress-linear",props:{active:{type:Boolean,default:!0},backgroundColor:{type:String,default:null},backgroundOpacity:{type:[Number,String],default:null},bufferValue:{type:[Number,String],default:100},color:{type:String,default:"primary"},height:{type:[Number,String],default:4},indeterminate:Boolean,query:Boolean,reverse:Boolean,rounded:Boolean,stream:Boolean,striped:Boolean,value:{type:[Number,String],default:0}},data:function(){return{internalLazyValue:this.value||0}},computed:{__cachedBackground:function(){return this.$createElement("div",this.setBackgroundColor(this.backgroundColor||this.color,{staticClass:"v-progress-linear__background",style:this.backgroundStyle}))},__cachedBar:function(){return this.$createElement(this.computedTransition,[this.__cachedBarType])},__cachedBarType:function(){return this.indeterminate?this.__cachedIndeterminate:this.__cachedDeterminate},__cachedBuffer:function(){return this.$createElement("div",{staticClass:"v-progress-linear__buffer",style:this.styles})},__cachedDeterminate:function(){return this.$createElement("div",this.setBackgroundColor(this.color,{staticClass:"v-progress-linear__determinate",style:{width:Object(v.g)(this.normalizedValue,"%")}}))},__cachedIndeterminate:function(){return this.$createElement("div",{staticClass:"v-progress-linear__indeterminate",class:{"v-progress-linear__indeterminate--active":this.active}},[this.genProgressBar("long"),this.genProgressBar("short")])},__cachedStream:function(){return this.stream?this.$createElement("div",this.setTextColor(this.color,{staticClass:"v-progress-linear__stream",style:{width:Object(v.g)(100-this.normalizedBuffer,"%")}})):null},backgroundStyle:function(){var t;return t={opacity:null==this.backgroundOpacity?this.backgroundColor?1:.3:parseFloat(this.backgroundOpacity)},Object(o.a)(t,this.isReversed?"right":"left",Object(v.g)(this.normalizedValue,"%")),Object(o.a)(t,"width",Object(v.g)(this.normalizedBuffer-this.normalizedValue,"%")),t},classes:function(){return function(t){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?_(Object(source),!0).forEach((function(e){Object(o.a)(t,e,source[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(source)):_(Object(source)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(source,e))}))}return t}({"v-progress-linear--absolute":this.absolute,"v-progress-linear--fixed":this.fixed,"v-progress-linear--query":this.query,"v-progress-linear--reactive":this.reactive,"v-progress-linear--reverse":this.isReversed,"v-progress-linear--rounded":this.rounded,"v-progress-linear--striped":this.striped},this.themeClasses)},computedTransition:function(){return this.indeterminate?l.d:l.f},isReversed:function(){return this.$vuetify.rtl!==this.reverse},normalizedBuffer:function(){return this.normalize(this.bufferValue)},normalizedValue:function(){return this.normalize(this.internalLazyValue)},reactive:function(){return Boolean(this.$listeners.change)},styles:function(){var t={};return this.active||(t.height=0),this.indeterminate||100===parseFloat(this.normalizedBuffer)||(t.width=Object(v.g)(this.normalizedBuffer,"%")),t}},methods:{genContent:function(){var slot=Object(v.s)(this,"default",{value:this.internalLazyValue});return slot?this.$createElement("div",{staticClass:"v-progress-linear__content"},slot):null},genListeners:function(){var t=this.$listeners;return this.reactive&&(t.click=this.onClick),t},genProgressBar:function(t){return this.$createElement("div",this.setBackgroundColor(this.color,{staticClass:"v-progress-linear__indeterminate",class:Object(o.a)({},t,!0)}))},onClick:function(t){if(this.reactive){var e=this.$el.getBoundingClientRect().width;this.internalValue=t.offsetX/e*100}},normalize:function(t){return t<0?0:t>100?100:parseFloat(t)}},render:function(t){return t("div",{staticClass:"v-progress-linear",attrs:{role:"progressbar","aria-valuemin":0,"aria-valuemax":this.normalizedBuffer,"aria-valuenow":this.indeterminate?void 0:this.normalizedValue},class:this.classes,style:{bottom:this.bottom?0:void 0,height:this.active?Object(v.g)(this.height):0,top:this.top?0:void 0},on:this.genListeners()},[this.__cachedStream,this.__cachedBackground,this.__cachedBuffer,this.__cachedBar,this.genContent()])}});e.a=n.default.extend().extend({name:"loadable",props:{loading:{type:[Boolean,String],default:!1},loaderHeight:{type:[Number,String],default:2}},methods:{genProgress:function(){return!1===this.loading?null:this.$slots.progress||this.$createElement(x,{props:{absolute:!0,color:!0===this.loading||""===this.loading?this.color||"primary":this.loading,height:this.loaderHeight,indeterminate:!0}})}}})},508:function(t,e,r){"use strict";r(15),r(11),r(9),r(7),r(12);var n=r(5),o=(r(28),r(519),r(184)),l=r(507),c=r(74),d=r(13);function h(object,t){var e=Object.keys(object);if(Object.getOwnPropertySymbols){var r=Object.getOwnPropertySymbols(object);t&&(r=r.filter((function(t){return Object.getOwnPropertyDescriptor(object,t).enumerable}))),e.push.apply(e,r)}return e}function f(t){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?h(Object(source),!0).forEach((function(e){Object(n.a)(t,e,source[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(source)):h(Object(source)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(source,e))}))}return t}e.a=Object(d.a)(l.a,c.a,o.a).extend({name:"v-card",props:{flat:Boolean,hover:Boolean,img:String,link:Boolean,loaderHeight:{type:[Number,String],default:4},raised:Boolean},computed:{classes:function(){return f(f({"v-card":!0},c.a.options.computed.classes.call(this)),{},{"v-card--flat":this.flat,"v-card--hover":this.hover,"v-card--link":this.isClickable,"v-card--loading":this.loading,"v-card--disabled":this.disabled,"v-card--raised":this.raised},o.a.options.computed.classes.call(this))},styles:function(){var style=f({},o.a.options.computed.styles.call(this));return this.img&&(style.background='url("'.concat(this.img,'") center center / cover no-repeat')),style}},methods:{genProgress:function(){var t=l.a.options.methods.genProgress.call(this);return t?this.$createElement("div",{staticClass:"v-card__progress",key:"progress"},[t]):null}},render:function(t){var e=this.generateRouteLink(),r=e.tag,data=e.data;return data.style=this.styles,this.isClickable&&(data.attrs=data.attrs||{},data.attrs.tabindex=0),t(r,this.setBackgroundColor(this.color,data),[this.genProgress(),this.$slots.default])}})},519:function(t,e,r){var content=r(520);"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,r(24).default)("e23b7040",content,!0,{sourceMap:!1})},520:function(t,e,r){(e=r(23)(!1)).push([t.i,'.theme--light.v-card{background-color:#fff;color:rgba(0,0,0,.87)}.theme--light.v-card .v-card__subtitle,.theme--light.v-card>.v-card__text{color:rgba(0,0,0,.6)}.theme--dark.v-card{background-color:#1e1e1e;color:#fff}.theme--dark.v-card .v-card__subtitle,.theme--dark.v-card>.v-card__text{color:hsla(0,0%,100%,.7)}.v-sheet.v-card{border-radius:4px}.v-sheet.v-card:not(.v-sheet--outlined){box-shadow:0 3px 1px -2px rgba(0,0,0,.2),0 2px 2px 0 rgba(0,0,0,.14),0 1px 5px 0 rgba(0,0,0,.12)}.v-sheet.v-card.v-sheet--shaped{border-radius:24px 4px}.v-card{border-width:thin;display:block;max-width:100%;outline:none;text-decoration:none;transition-property:box-shadow,opacity;word-wrap:break-word;position:relative;white-space:normal}.v-card>.v-card__progress+:not(.v-btn):not(.v-chip),.v-card>:first-child:not(.v-btn):not(.v-chip){border-top-left-radius:inherit;border-top-right-radius:inherit}.v-card>:last-child:not(.v-btn):not(.v-chip){border-bottom-left-radius:inherit;border-bottom-right-radius:inherit}.v-card__progress{top:0;left:0;right:0;overflow:hidden}.v-card__subtitle+.v-card__text{padding-top:0}.v-card__subtitle,.v-card__text{font-size:.875rem;font-weight:400;line-height:1.375rem;letter-spacing:.0071428571em}.v-card__subtitle,.v-card__text,.v-card__title{padding:16px}.v-card__title{align-items:center;display:flex;flex-wrap:wrap;font-size:1.25rem;font-weight:500;letter-spacing:.0125em;line-height:2rem;word-break:break-all}.v-card__title+.v-card__subtitle,.v-card__title+.v-card__text{padding-top:0}.v-card__title+.v-card__subtitle{margin-top:-16px}.v-card__text{width:100%}.v-card__actions{align-items:center;display:flex;padding:8px}.v-card__actions>.v-btn.v-btn{padding:0 8px}.v-application--is-ltr .v-card__actions>.v-btn.v-btn+.v-btn{margin-left:8px}.v-application--is-ltr .v-card__actions>.v-btn.v-btn .v-icon--left{margin-left:4px}.v-application--is-ltr .v-card__actions>.v-btn.v-btn .v-icon--right{margin-right:4px}.v-application--is-rtl .v-card__actions>.v-btn.v-btn+.v-btn{margin-right:8px}.v-application--is-rtl .v-card__actions>.v-btn.v-btn .v-icon--left{margin-right:4px}.v-application--is-rtl .v-card__actions>.v-btn.v-btn .v-icon--right{margin-left:4px}.v-card--flat{box-shadow:0 0 0 0 rgba(0,0,0,.2),0 0 0 0 rgba(0,0,0,.14),0 0 0 0 rgba(0,0,0,.12)!important}.v-card--hover{cursor:pointer;transition:box-shadow .4s cubic-bezier(.25,.8,.25,1)}.v-card--hover:focus,.v-card--hover:hover{box-shadow:0 5px 5px -3px rgba(0,0,0,.2),0 8px 10px 1px rgba(0,0,0,.14),0 3px 14px 2px rgba(0,0,0,.12)}.v-card--link,.v-card--link .v-chip{cursor:pointer}.v-card--link:focus:before{opacity:.08}.v-card--link:before{background:currentColor;bottom:0;content:"";left:0;opacity:0;pointer-events:none;position:absolute;right:0;top:0;transition:opacity .2s}.v-card--disabled{pointer-events:none;-webkit-user-select:none;-moz-user-select:none;-ms-user-select:none;user-select:none}.v-card--disabled>:not(.v-card__progress){opacity:.6;transition:inherit}.v-card--loading{overflow:hidden}.v-card--raised{box-shadow:0 5px 5px -3px rgba(0,0,0,.2),0 8px 10px 1px rgba(0,0,0,.14),0 3px 14px 2px rgba(0,0,0,.12)}',""]),t.exports=e},521:function(t,e,r){var content=r(522);"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,r(24).default)("cf87dc84",content,!0,{sourceMap:!1})},522:function(t,e,r){(e=r(23)(!1)).push([t.i,".theme--light.v-progress-linear{color:rgba(0,0,0,.87)}.theme--dark.v-progress-linear{color:#fff}.v-progress-linear{background:transparent;overflow:hidden;position:relative;transition:.2s cubic-bezier(.4,0,.6,1);width:100%}.v-progress-linear__buffer{height:inherit;left:0;position:absolute;top:0;transition:inherit;width:100%;z-index:1}.v-progress-linear--reverse .v-progress-linear__buffer{left:auto;right:0}.v-progress-linear__background{bottom:0;left:0;position:absolute;top:0;transition:inherit}.v-progress-linear--reverse .v-progress-linear__background{left:auto;right:0}.v-progress-linear__content{align-items:center;display:flex;height:100%;left:0;justify-content:center;position:absolute;top:0;width:100%;z-index:2}.v-progress-linear--reverse .v-progress-linear__content{left:auto;right:0}.v-progress-linear__determinate{height:inherit;left:0;position:absolute;transition:inherit}.v-progress-linear--reverse .v-progress-linear__determinate{left:auto;right:0}.v-progress-linear .v-progress-linear__indeterminate .long,.v-progress-linear .v-progress-linear__indeterminate .short{background-color:inherit;bottom:0;height:inherit;left:0;position:absolute;right:auto;top:0;width:auto;will-change:left,right}.v-progress-linear .v-progress-linear__indeterminate--active .long{-webkit-animation-name:indeterminate-ltr;animation-name:indeterminate-ltr;-webkit-animation-duration:2.2s;animation-duration:2.2s;-webkit-animation-iteration-count:infinite;animation-iteration-count:infinite}.v-progress-linear .v-progress-linear__indeterminate--active .short{-webkit-animation-name:indeterminate-short-ltr;animation-name:indeterminate-short-ltr;-webkit-animation-duration:2.2s;animation-duration:2.2s;-webkit-animation-iteration-count:infinite;animation-iteration-count:infinite}.v-progress-linear--reverse .v-progress-linear__indeterminate .long,.v-progress-linear--reverse .v-progress-linear__indeterminate .short{left:auto;right:0}.v-progress-linear--reverse .v-progress-linear__indeterminate--active .long{-webkit-animation-name:indeterminate-rtl;animation-name:indeterminate-rtl}.v-progress-linear--reverse .v-progress-linear__indeterminate--active .short{-webkit-animation-name:indeterminate-short-rtl;animation-name:indeterminate-short-rtl}.v-progress-linear__stream{-webkit-animation:stream-ltr .25s linear infinite;animation:stream-ltr .25s linear infinite;border-color:currentColor;border-top:4px dotted;bottom:0;left:auto;right:-8px;opacity:.3;pointer-events:none;position:absolute;top:calc(50% - 2px);transition:inherit}.v-progress-linear--reverse .v-progress-linear__stream{-webkit-animation:stream-rtl .25s linear infinite;animation:stream-rtl .25s linear infinite;left:-8px;right:auto}.v-progress-linear__wrapper{overflow:hidden;position:relative;transition:inherit}.v-progress-linear--absolute,.v-progress-linear--fixed{left:0;z-index:1}.v-progress-linear--absolute{position:absolute}.v-progress-linear--fixed{position:fixed}.v-progress-linear--reactive .v-progress-linear__content{pointer-events:none}.v-progress-linear--rounded{border-radius:4px}.v-progress-linear--striped .v-progress-linear__determinate{background-image:linear-gradient(135deg,hsla(0,0%,100%,.25) 25%,transparent 0,transparent 50%,hsla(0,0%,100%,.25) 0,hsla(0,0%,100%,.25) 75%,transparent 0,transparent);background-size:40px 40px;background-repeat:repeat}.v-progress-linear--query .v-progress-linear__indeterminate--active .long{-webkit-animation-name:query-ltr;animation-name:query-ltr;-webkit-animation-duration:2s;animation-duration:2s;-webkit-animation-iteration-count:infinite;animation-iteration-count:infinite}.v-progress-linear--query .v-progress-linear__indeterminate--active .short{-webkit-animation-name:query-short-ltr;animation-name:query-short-ltr;-webkit-animation-duration:2s;animation-duration:2s;-webkit-animation-iteration-count:infinite;animation-iteration-count:infinite}.v-progress-linear--query.v-progress-linear--reverse .v-progress-linear__indeterminate--active .long{-webkit-animation-name:query-rtl;animation-name:query-rtl}.v-progress-linear--query.v-progress-linear--reverse .v-progress-linear__indeterminate--active .short{-webkit-animation-name:query-short-rtl;animation-name:query-short-rtl}@-webkit-keyframes indeterminate-ltr{0%{left:-90%;right:100%}60%{left:-90%;right:100%}to{left:100%;right:-35%}}@keyframes indeterminate-ltr{0%{left:-90%;right:100%}60%{left:-90%;right:100%}to{left:100%;right:-35%}}@-webkit-keyframes indeterminate-rtl{0%{left:100%;right:-90%}60%{left:100%;right:-90%}to{left:-35%;right:100%}}@keyframes indeterminate-rtl{0%{left:100%;right:-90%}60%{left:100%;right:-90%}to{left:-35%;right:100%}}@-webkit-keyframes indeterminate-short-ltr{0%{left:-200%;right:100%}60%{left:107%;right:-8%}to{left:107%;right:-8%}}@keyframes indeterminate-short-ltr{0%{left:-200%;right:100%}60%{left:107%;right:-8%}to{left:107%;right:-8%}}@-webkit-keyframes indeterminate-short-rtl{0%{left:100%;right:-200%}60%{left:-8%;right:107%}to{left:-8%;right:107%}}@keyframes indeterminate-short-rtl{0%{left:100%;right:-200%}60%{left:-8%;right:107%}to{left:-8%;right:107%}}@-webkit-keyframes query-ltr{0%{right:-90%;left:100%}60%{right:-90%;left:100%}to{right:100%;left:-35%}}@keyframes query-ltr{0%{right:-90%;left:100%}60%{right:-90%;left:100%}to{right:100%;left:-35%}}@-webkit-keyframes query-rtl{0%{right:100%;left:-90%}60%{right:100%;left:-90%}to{right:-35%;left:100%}}@keyframes query-rtl{0%{right:100%;left:-90%}60%{right:100%;left:-90%}to{right:-35%;left:100%}}@-webkit-keyframes query-short-ltr{0%{right:-200%;left:100%}60%{right:107%;left:-8%}to{right:107%;left:-8%}}@keyframes query-short-ltr{0%{right:-200%;left:100%}60%{right:107%;left:-8%}to{right:107%;left:-8%}}@-webkit-keyframes query-short-rtl{0%{right:100%;left:-200%}60%{right:-8%;left:107%}to{right:-8%;left:107%}}@keyframes query-short-rtl{0%{right:100%;left:-200%}60%{right:-8%;left:107%}to{right:-8%;left:107%}}@-webkit-keyframes stream-ltr{to{transform:translateX(-8px)}}@keyframes stream-ltr{to{transform:translateX(-8px)}}@-webkit-keyframes stream-rtl{to{transform:translateX(8px)}}@keyframes stream-rtl{to{transform:translateX(8px)}}",""]),t.exports=e},532:function(t,e,r){var content=r(567);"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,r(24).default)("a638c6ec",content,!0,{sourceMap:!1})},567:function(t,e,r){(e=r(23)(!1)).push([t.i,".theme--dark .tui-editor-contents h1{color:#fff}.theme--dark .tui-editor-contents code span,.theme--dark .tui-editor-contents h2,.theme--dark .tui-editor-contents h3,.theme--dark .tui-editor-contents h4,.theme--dark .tui-editor-contents h5,.theme--dark .tui-editor-contents h6{color:#ccc}.theme--dark .tui-editor-contents blockquote{color:#888}.theme--dark .tui-editor-contents dir,.theme--dark .tui-editor-contents menu,.theme--dark .tui-editor-contents ol,.theme--dark .tui-editor-contents p,.theme--dark .tui-editor-contents table,.theme--dark .tui-editor-contents ul{color:#aaa}.theme--dark .tui-editor-contents table td{border:#151515}.theme--dark .tui-editor-contents table th{border:#8d8884;background-color:#847e7b}.theme--dark .tui-editor-contents pre{background-color:#0a0807}.theme--dark .tui-editor-contents code{color:#3e8774}",""]),t.exports=e},568:function(t,e,r){t.exports=r.p+"img/vbanner.0d5edfa.jpg"},605:function(t,e,r){t.exports=r.p+"img/ner_demo.de1202e.png"},763:function(t,e,r){var map={"./feature1.png":764,"./feature2.png":765,"./feature3.png":766,"./icon.png":336,"./ner_demo.png":605,"./style/editor.css":532,"./vbanner.jpg":568};function n(t){var e=o(t);return r(e)}function o(t){if(!r.o(map,t)){var e=new Error("Cannot find module '"+t+"'");throw e.code="MODULE_NOT_FOUND",e}return map[t]}n.keys=function(){return Object.keys(map)},n.resolve=o,t.exports=n,n.id=763},764:function(t,e,r){t.exports=r.p+"img/feature1.73f716e.png"},765:function(t,e,r){t.exports=r.p+"img/feature2.f6f8d1a.png"},766:function(t,e,r){t.exports=r.p+"img/feature3.c3a7495.png"},767:function(t,e,r){var content=r(768);"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,r(24).default)("0cd63bd9",content,!0,{sourceMap:!1})},768:function(t,e,r){(e=r(23)(!1)).push([t.i,".v-parallax{position:relative;overflow:hidden;z-index:0}.v-parallax__image-container{position:absolute;top:0;left:0;right:0;bottom:0;z-index:1;contain:strict}.v-parallax__image{position:absolute;bottom:0;left:50%;min-width:100%;min-height:100%;display:none;transform:translate(-50%);will-change:transform;transition:opacity .3s cubic-bezier(.25,.8,.5,1);z-index:1}.v-parallax__content{color:#fff;height:100%;z-index:2;position:relative;display:flex;flex-direction:column;justify-content:center;padding:0 1rem}",""]),t.exports=e}}]);