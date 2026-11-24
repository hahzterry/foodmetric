import type {Metadata} from "next";
import "./globals.css";
export const metadata:Metadata={title:"FoodMetric USA | Trending TikTok Shop Food",description:"Discover trending snacks and beverages in the US market.",openGraph:{locale:"en_US",type:"website",title:"FoodMetric USA"}};
export default function RootLayout({children}:{children:React.ReactNode}){return <html lang="en-US"><body className="min-h-screen bg-slate-50 text-slate-900">{children}</body></html>}
