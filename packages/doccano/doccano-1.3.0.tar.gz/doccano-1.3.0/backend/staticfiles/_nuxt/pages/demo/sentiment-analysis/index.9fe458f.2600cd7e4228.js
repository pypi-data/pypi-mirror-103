(window.webpackJsonp=window.webpackJsonp||[]).push([[100],{1109:function(t,e,n){"use strict";n.r(e);n(28),n(527);var r=n(500),o={layout:"demo",components:{LabelGroup:n(596).a,ListMetadata:r.a},data:function(){return{items:[{id:4,text:"Positive",prefixKey:null,suffixKey:"p",backgroundColor:"#7c20e0",textColor:"#ffffff"},{id:5,text:"Negative",prefixKey:null,suffixKey:"n",backgroundColor:"#fbb028",textColor:"#000000"}],currentDoc:{id:8,text:"Fair drama/love story movie that focuses on the lives of blue collar people finding new life thru new love. The acting here is good but the film fails in cinematography, screenplay, directing and editing. The story/script is only average at best. This film will be enjoyed by Fonda and De Niro fans and by people who love middle age love stories where in the coartship is on a more wiser and cautious level. It would also be interesting for people who are interested on the subject matter regarding illiteracy.......",annotations:[{id:17,prob:0,label:4,user:1,document:8}],meta:'{"wikiPageId":2}',annotation_approver:null}}},methods:{removeLabel:function(t){this.currentDoc.annotations=this.currentDoc.annotations.filter((function(e){return e.id!==t}))},addLabel:function(t){var e={id:Math.floor(Math.random()*Math.floor(Number.MAX_SAFE_INTEGER)),label:t};this.currentDoc.annotations.push(e)}}},l=n(27),c=n(31),f=n.n(c),d=n(508),h=n(491),v=n(509),m=n(482),y=n(607),O=n(488),w=n(510),component=Object(l.a)(o,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-main",[n("v-container",{attrs:{fluid:""}},[n("v-row",{attrs:{justify:"center"}},[n("v-col",{attrs:{cols:"12",md:"9"}},[n("v-card",[n("v-card-title",[n("label-group",{attrs:{labels:t.items,annotations:t.currentDoc.annotations,"single-label":"true"},on:{add:t.addLabel,remove:t.removeLabel}})],1),t._v(" "),n("v-divider"),t._v(" "),n("v-card-text",{staticClass:"title"},[t._v("\n            "+t._s(t.currentDoc.text)+"\n          ")])],1)],1),t._v(" "),n("v-col",{attrs:{cols:"12",md:"3"}},[n("list-metadata",{attrs:{metadata:t.currentDoc.meta}})],1)],1)],1)],1)}),[],!1,null,null,null);e.default=component.exports;f()(component,{VCard:d.a,VCardText:h.b,VCardTitle:h.c,VCol:v.a,VContainer:m.a,VDivider:y.a,VMain:O.a,VRow:w.a})},500:function(t,e,n){"use strict";var r=n(17),o=(n(9),n(7),n(142),n(3).default.extend({props:{metadata:{type:Object,default:function(){return{}},required:!0}},data:function(){return{headers:[{text:this.$t("annotation.key"),align:"left",value:"key",sortable:!1},{text:this.$t("annotation.value"),align:"left",value:"value",sortable:!1}]}},computed:{metaArray:function(){for(var t=[],e=0,n=Object.entries(this.metadata);e<n.length;e++){var o=Object(r.a)(n[e],2),l=o[0],c=o[1];t.push({key:l,value:c})}return t}}})),l=n(27),c=n(31),f=n.n(c),d=n(1104),component=Object(l.a)(o,(function(){var t=this.$createElement;return(this._self._c||t)("v-data-table",{staticClass:"elevation-1",attrs:{headers:this.headers,items:this.metaArray,"item-key":"key","hide-default-footer":"","no-data-text":this.$t("vuetify.noDataAvailable"),"disable-pagination":""}})}),[],!1,null,null,null);e.a=component.exports;f()(component,{VDataTable:d.a})},509:function(t,e,n){"use strict";n(15),n(11),n(65),n(33),n(34);var r=n(5),o=(n(41),n(181),n(52),n(9),n(7),n(12),n(28),n(246),n(3)),l=n(73),c=n(4);function f(object,t){var e=Object.keys(object);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(object);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(object,t).enumerable}))),e.push.apply(e,n)}return e}function d(t){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?f(Object(source),!0).forEach((function(e){Object(r.a)(t,e,source[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(source)):f(Object(source)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(source,e))}))}return t}var h=["sm","md","lg","xl"],v=h.reduce((function(t,e){return t[e]={type:[Boolean,String,Number],default:!1},t}),{}),m=h.reduce((function(t,e){return t["offset"+Object(c.G)(e)]={type:[String,Number],default:null},t}),{}),y=h.reduce((function(t,e){return t["order"+Object(c.G)(e)]={type:[String,Number],default:null},t}),{}),O={col:Object.keys(v),offset:Object.keys(m),order:Object.keys(y)};function w(t,e,n){var r=t;if(null!=n&&!1!==n){if(e){var o=e.replace(t,"");r+="-".concat(o)}return"col"!==t||""!==n&&!0!==n?(r+="-".concat(n)).toLowerCase():r.toLowerCase()}}var x=new Map;e.a=o.default.extend({name:"v-col",functional:!0,props:d(d(d(d({cols:{type:[Boolean,String,Number],default:!1}},v),{},{offset:{type:[String,Number],default:null}},m),{},{order:{type:[String,Number],default:null}},y),{},{alignSelf:{type:String,default:null,validator:function(t){return["auto","start","end","center","baseline","stretch"].includes(t)}},tag:{type:String,default:"div"}}),render:function(t,e){var n=e.props,data=e.data,o=e.children,c=(e.parent,"");for(var f in n)c+=String(n[f]);var d=x.get(c);return d||function(){var t,e;for(e in d=[],O)O[e].forEach((function(t){var r=n[t],o=w(e,t,r);o&&d.push(o)}));var o=d.some((function(t){return t.startsWith("col-")}));d.push((t={col:!o||!n.cols},Object(r.a)(t,"col-".concat(n.cols),n.cols),Object(r.a)(t,"offset-".concat(n.offset),n.offset),Object(r.a)(t,"order-".concat(n.order),n.order),Object(r.a)(t,"align-self-".concat(n.alignSelf),n.alignSelf),t)),x.set(c,d)}(),t(n.tag,Object(l.a)(data,{class:d}),o)}})},510:function(t,e,n){"use strict";n(15),n(11);var r=n(5),o=(n(41),n(181),n(52),n(9),n(7),n(12),n(33),n(34),n(246),n(3)),l=n(73),c=n(4);function f(object,t){var e=Object.keys(object);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(object);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(object,t).enumerable}))),e.push.apply(e,n)}return e}function d(t){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?f(Object(source),!0).forEach((function(e){Object(r.a)(t,e,source[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(source)):f(Object(source)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(source,e))}))}return t}var h=["sm","md","lg","xl"],v=["start","end","center"];function m(t,e){return h.reduce((function(n,r){return n[t+Object(c.G)(r)]=e(),n}),{})}var y=function(t){return[].concat(v,["baseline","stretch"]).includes(t)},O=m("align",(function(){return{type:String,default:null,validator:y}})),w=function(t){return[].concat(v,["space-between","space-around"]).includes(t)},x=m("justify",(function(){return{type:String,default:null,validator:w}})),j=function(t){return[].concat(v,["space-between","space-around","stretch"]).includes(t)},_=m("alignContent",(function(){return{type:String,default:null,validator:j}})),C={align:Object.keys(O),justify:Object.keys(x),alignContent:Object.keys(_)},$={align:"align",justify:"justify",alignContent:"align-content"};function P(t,e,n){var r=$[t];if(null!=n){if(e){var o=e.replace(t,"");r+="-".concat(o)}return(r+="-".concat(n)).toLowerCase()}}var k=new Map;e.a=o.default.extend({name:"v-row",functional:!0,props:d(d(d({tag:{type:String,default:"div"},dense:Boolean,noGutters:Boolean,align:{type:String,default:null,validator:y}},O),{},{justify:{type:String,default:null,validator:w}},x),{},{alignContent:{type:String,default:null,validator:j}},_),render:function(t,e){var n=e.props,data=e.data,o=e.children,c="";for(var f in n)c+=String(n[f]);var d=k.get(c);return d||function(){var t,e;for(e in d=[],C)C[e].forEach((function(t){var r=n[t],o=P(e,t,r);o&&d.push(o)}));d.push((t={"no-gutters":n.noGutters,"row--dense":n.dense},Object(r.a)(t,"align-".concat(n.align),n.align),Object(r.a)(t,"justify-".concat(n.justify),n.justify),Object(r.a)(t,"align-content-".concat(n.alignContent),n.alignContent),t)),k.set(c,d)}(),t(n.tag,Object(l.a)(data,{staticClass:"row",class:d}),o)}})},527:function(t,e,n){var r=n(26);r(r.S,"Number",{MAX_SAFE_INTEGER:9007199254740991})},538:function(t,e,n){"use strict";n.d(e,"a",(function(){return O}));n(15),n(11),n(9),n(7),n(12);var r=n(5),o=(n(33),n(34),n(539),n(64)),l=n(183),c=n(116),f=n(146),d=n(121),h=n(188),v=n(13);function m(object,t){var e=Object.keys(object);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(object);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(object,t).enumerable}))),e.push.apply(e,n)}return e}function y(t){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?m(Object(source),!0).forEach((function(e){Object(r.a)(t,e,source[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(source)):m(Object(source)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(source,e))}))}return t}var O=Object(v.a)(c.a,f.a).extend({name:"base-slide-group",directives:{Resize:d.a,Touch:h.a},props:{activeClass:{type:String,default:"v-slide-item--active"},centerActive:Boolean,nextIcon:{type:String,default:"$next"},prevIcon:{type:String,default:"$prev"},showArrows:{type:[Boolean,String],validator:function(t){return"boolean"==typeof t||["always","desktop","mobile"].includes(t)}}},data:function(){return{internalItemsLength:0,isOverflowing:!1,resizeTimeout:0,startX:0,scrollOffset:0,widths:{content:0,wrapper:0}}},computed:{__cachedNext:function(){return this.genTransition("next")},__cachedPrev:function(){return this.genTransition("prev")},classes:function(){return y(y({},c.a.options.computed.classes.call(this)),{},{"v-slide-group":!0,"v-slide-group--has-affixes":this.hasAffixes,"v-slide-group--is-overflowing":this.isOverflowing})},hasAffixes:function(){switch(this.showArrows){case"always":return!0;case"desktop":return!this.isMobile;case!0:return this.isOverflowing;case"mobile":return this.isMobile||this.isOverflowing;default:return!this.isMobile&&this.isOverflowing}},hasNext:function(){if(!this.hasAffixes)return!1;var t=this.widths,content=t.content,e=t.wrapper;return content>Math.abs(this.scrollOffset)+e},hasPrev:function(){return this.hasAffixes&&0!==this.scrollOffset}},watch:{internalValue:"setWidths",isOverflowing:"setWidths",scrollOffset:function(t){this.$refs.content.style.transform="translateX(".concat(-t,"px)")}},beforeUpdate:function(){this.internalItemsLength=(this.$children||[]).length},updated:function(){this.internalItemsLength!==(this.$children||[]).length&&this.setWidths()},methods:{genNext:function(){var t=this,slot=this.$scopedSlots.next?this.$scopedSlots.next({}):this.$slots.next||this.__cachedNext;return this.$createElement("div",{staticClass:"v-slide-group__next",class:{"v-slide-group__next--disabled":!this.hasNext},on:{click:function(){return t.onAffixClick("next")}},key:"next"},[slot])},genContent:function(){return this.$createElement("div",{staticClass:"v-slide-group__content",ref:"content"},this.$slots.default)},genData:function(){return{class:this.classes,directives:[{name:"resize",value:this.onResize}]}},genIcon:function(t){var e=t;this.$vuetify.rtl&&"prev"===t?e="next":this.$vuetify.rtl&&"next"===t&&(e="prev");var n="".concat(t[0].toUpperCase()).concat(t.slice(1)),r=this["has".concat(n)];return this.showArrows||r?this.$createElement(o.a,{props:{disabled:!r}},this["".concat(e,"Icon")]):null},genPrev:function(){var t=this,slot=this.$scopedSlots.prev?this.$scopedSlots.prev({}):this.$slots.prev||this.__cachedPrev;return this.$createElement("div",{staticClass:"v-slide-group__prev",class:{"v-slide-group__prev--disabled":!this.hasPrev},on:{click:function(){return t.onAffixClick("prev")}},key:"prev"},[slot])},genTransition:function(t){return this.$createElement(l.d,[this.genIcon(t)])},genWrapper:function(){var t=this;return this.$createElement("div",{staticClass:"v-slide-group__wrapper",directives:[{name:"touch",value:{start:function(e){return t.overflowCheck(e,t.onTouchStart)},move:function(e){return t.overflowCheck(e,t.onTouchMove)},end:function(e){return t.overflowCheck(e,t.onTouchEnd)}}}],ref:"wrapper"},[this.genContent()])},calculateNewOffset:function(t,e,n,r){var o=n?-1:1,l=o*r+("prev"===t?-1:1)*e.wrapper;return o*Math.max(Math.min(l,e.content-e.wrapper),0)},onAffixClick:function(t){this.$emit("click:".concat(t)),this.scrollTo(t)},onResize:function(){this._isDestroyed||this.setWidths()},onTouchStart:function(t){var content=this.$refs.content;this.startX=this.scrollOffset+t.touchstartX,content.style.setProperty("transition","none"),content.style.setProperty("willChange","transform")},onTouchMove:function(t){this.scrollOffset=this.startX-t.touchmoveX},onTouchEnd:function(){var t=this.$refs,content=t.content,e=t.wrapper,n=content.clientWidth-e.clientWidth;content.style.setProperty("transition",null),content.style.setProperty("willChange",null),this.$vuetify.rtl?this.scrollOffset>0||!this.isOverflowing?this.scrollOffset=0:this.scrollOffset<=-n&&(this.scrollOffset=-n):this.scrollOffset<0||!this.isOverflowing?this.scrollOffset=0:this.scrollOffset>=n&&(this.scrollOffset=n)},overflowCheck:function(t,e){t.stopPropagation(),this.isOverflowing&&e(t)},scrollIntoView:function(){this.selectedItem&&(0===this.selectedIndex||!this.centerActive&&!this.isOverflowing?this.scrollOffset=0:this.centerActive?this.scrollOffset=this.calculateCenteredOffset(this.selectedItem.$el,this.widths,this.$vuetify.rtl):this.isOverflowing&&(this.scrollOffset=this.calculateUpdatedOffset(this.selectedItem.$el,this.widths,this.$vuetify.rtl,this.scrollOffset)))},calculateUpdatedOffset:function(t,e,n,r){var o=t.clientWidth,l=n?e.content-t.offsetLeft-o:t.offsetLeft;n&&(r=-r);var c=e.wrapper+r,f=o+l,d=.4*o;return l<r?r=Math.max(l-d,0):c<f&&(r=Math.min(r-(c-f-d),e.content-e.wrapper)),n?-r:r},calculateCenteredOffset:function(t,e,n){var r=t.offsetLeft,o=t.clientWidth;if(n){var l=e.content-r-o/2-e.wrapper/2;return-Math.min(e.content-e.wrapper,Math.max(0,l))}var c=r+o/2-e.wrapper/2;return Math.min(e.content-e.wrapper,Math.max(0,c))},scrollTo:function(t){this.scrollOffset=this.calculateNewOffset(t,{content:this.$refs.content?this.$refs.content.clientWidth:0,wrapper:this.$refs.wrapper?this.$refs.wrapper.clientWidth:0},this.$vuetify.rtl,this.scrollOffset)},setWidths:function(){var t=this;window.requestAnimationFrame((function(){var e=t.$refs,content=e.content,n=e.wrapper;t.widths={content:content?content.clientWidth:0,wrapper:n?n.clientWidth:0},t.isOverflowing=t.widths.wrapper<t.widths.content,t.scrollIntoView()}))}},render:function(t){return t("div",this.genData(),[this.genPrev(),this.genWrapper(),this.genNext()])}});O.extend({name:"v-slide-group",provide:function(){return{slideGroup:this}}})},539:function(t,e,n){var content=n(540);"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,n(24).default)("8f7a87bc",content,!0,{sourceMap:!1})},540:function(t,e,n){(e=n(23)(!1)).push([t.i,".v-slide-group{display:flex}.v-slide-group:not(.v-slide-group--has-affixes)>.v-slide-group__next,.v-slide-group:not(.v-slide-group--has-affixes)>.v-slide-group__prev{display:none}.v-slide-group.v-item-group>.v-slide-group__next,.v-slide-group.v-item-group>.v-slide-group__prev{cursor:pointer}.v-slide-item{display:inline-flex;flex:0 1 auto}.v-slide-group__next,.v-slide-group__prev{align-items:center;display:flex;flex:0 1 52px;justify-content:center;min-width:52px}.v-slide-group__content{display:flex;flex:1 0 auto;position:relative;transition:.3s cubic-bezier(.25,.8,.5,1);white-space:nowrap}.v-slide-group__wrapper{contain:content;display:flex;flex:1 1 auto;overflow:hidden;touch-action:none}.v-slide-group__next--disabled,.v-slide-group__prev--disabled{pointer-events:none}",""]),t.exports=e},577:function(t,e,n){var content=n(578);"string"==typeof content&&(content=[[t.i,content,""]]),content.locals&&(t.exports=content.locals);(0,n(24).default)("3c0eddd7",content,!0,{sourceMap:!1})},578:function(t,e,n){(e=n(23)(!1)).push([t.i,".v-chip-group .v-chip{margin:4px 8px 4px 0}.v-chip-group .v-chip--active{color:inherit}.v-chip-group .v-chip--active.v-chip--no-color:after{opacity:.22}.v-chip-group .v-chip--active.v-chip--no-color:focus:after{opacity:.32}.v-chip-group .v-slide-group__content{padding:4px 0}.v-chip-group--column .v-slide-group__content{white-space:normal;flex-wrap:wrap;max-width:100%}",""]),t.exports=e},596:function(t,e,n){"use strict";n(55),n(33),n(34),n(113);var r={props:{labels:{type:Array,default:function(){return[]},required:!0},annotations:{type:Array,default:function(){return[]},required:!0}},computed:{annotatedLabel:function(){var t=this.annotations.map((function(t){return t.label}));return this.labels.findIndex((function(e){return t.includes(e.id)}))}},methods:{addOrRemove:function(t){if(void 0===t){var label=this.labels[this.annotatedLabel];this.remove(label)}else{var e=this.labels[t];this.add(e)}},add:function(label){this.$emit("add",label.id)},remove:function(label){var t=this.annotations.find((function(t){return t.label===label.id}));this.$emit("remove",t.id)}}},o=n(27),l=n(31),c=n.n(l),f=n(174),d=n(606),h=(n(15),n(11),n(9),n(7),n(12),n(5)),v=(n(577),n(538)),m=n(35),y=n(13);function O(object,t){var e=Object.keys(object);if(Object.getOwnPropertySymbols){var n=Object.getOwnPropertySymbols(object);t&&(n=n.filter((function(t){return Object.getOwnPropertyDescriptor(object,t).enumerable}))),e.push.apply(e,n)}return e}function w(t){for(var i=1;i<arguments.length;i++){var source=null!=arguments[i]?arguments[i]:{};i%2?O(Object(source),!0).forEach((function(e){Object(h.a)(t,e,source[e])})):Object.getOwnPropertyDescriptors?Object.defineProperties(t,Object.getOwnPropertyDescriptors(source)):O(Object(source)).forEach((function(e){Object.defineProperty(t,e,Object.getOwnPropertyDescriptor(source,e))}))}return t}var x=Object(y.a)(v.a,m.a).extend({name:"v-chip-group",provide:function(){return{chipGroup:this}},props:{column:Boolean},computed:{classes:function(){return w(w({},v.a.options.computed.classes.call(this)),{},{"v-chip-group":!0,"v-chip-group--column":this.column})}},watch:{column:function(t){t&&(this.scrollOffset=0),this.$nextTick(this.onResize)}},methods:{genData:function(){return this.setTextColor(this.color,w({},v.a.options.methods.genData.call(this)))}}}),component=Object(o.a)(r,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-chip-group",{attrs:{value:t.annotatedLabel,column:""},on:{change:t.addOrRemove}},t._l(t.labels,(function(e){return n("v-chip",{key:e.id,attrs:{color:e.backgroundColor,filter:"","text-color":t.$contrastColor(e.backgroundColor)}},[t._v("\n    "+t._s(e.text)+"\n    "),n("v-avatar",{staticClass:"black--text font-weight-bold",attrs:{right:"",color:"white"}},[t._v("\n      "+t._s(e.suffixKey)+"\n    ")])],1)})),1)}),[],!1,null,null,null),j=component.exports;c()(component,{VAvatar:f.a,VChip:d.a,VChipGroup:x});var _=n(186),C=n.n(_),$={props:{labels:{type:Array,default:function(){return[]},required:!0},annotations:{type:Array,default:function(){return[]},required:!0}},computed:{annotatedLabel:function(){var t=this;return this.annotations.map((function(t){return t.label})).map((function(e){return t.labels.findIndex((function(t){return t.id===e}))}))}},methods:{addOrRemove:function(t){if(t.length>this.annotatedLabel.length){var e=C.a.difference(t,this.annotatedLabel),label=this.labels[e];this.add(label)}else{var n=C.a.difference(this.annotatedLabel,t),r=this.labels[n];this.remove(r)}},add:function(label){this.$emit("add",label.id)},remove:function(label){var t=this.annotations.find((function(t){return t.label===label.id}));this.$emit("remove",t.id)}}},P=Object(o.a)($,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("v-chip-group",{attrs:{value:t.annotatedLabel,column:"",multiple:""},on:{change:t.addOrRemove}},t._l(t.labels,(function(e){return n("v-chip",{key:e.id,attrs:{color:e.backgroundColor,filter:"","text-color":t.$contrastColor(e.backgroundColor)}},[t._v("\n    "+t._s(e.text)+"\n    "),n("v-avatar",{staticClass:"black--text font-weight-bold",attrs:{right:"",color:"white"}},[t._v("\n      "+t._s(e.suffixKey)+"\n    ")])],1)})),1)}),[],!1,null,null,null),k=P.exports;c()(P,{VAvatar:f.a,VChip:d.a,VChipGroup:x});var S={components:{LabelGroupSingle:j,LabelGroupMulti:k},props:{labels:{type:Array,default:function(){return[]},required:!0},annotations:{type:Array,default:function(){return[]},required:!0},singleLabel:{type:Boolean,default:!1,required:!0}}},D=Object(o.a)(S,(function(){var t=this,e=t.$createElement,n=t._self._c||e;return t.singleLabel?n("label-group-single",{attrs:{annotations:t.annotations,labels:t.labels},on:{add:function(e){return t.$emit("add",e)},remove:function(e){return t.$emit("remove",e)}}}):n("label-group-multi",{attrs:{annotations:t.annotations,labels:t.labels},on:{add:function(e){return t.$emit("add",e)},remove:function(e){return t.$emit("remove",e)}}})}),[],!1,null,null,null);e.a=D.exports}}]);