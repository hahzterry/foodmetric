import type {MetadataRoute} from "next";
export default function manifest():MetadataRoute.Manifest{return {name:"FoodMetric USA",short_name:"FoodMetric",description:"US food and snack trends",lang:"en-US",start_url:"/",display:"standalone",background_color:"#ffffff",theme_color:"#ea580c",icons:[{src:"/icon.png",sizes:"512x512",type:"image/png"}]};}
