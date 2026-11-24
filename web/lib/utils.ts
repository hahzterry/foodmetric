import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";
export const cn = (...inputs: ClassValue[]) => twMerge(clsx(inputs));
export const formatUSD = (cents: number) => new Intl.NumberFormat("en-US", {style:"currency",currency:"USD"}).format(cents/100);
export const formatNumber = (n: number) => new Intl.NumberFormat("en-US").format(n);
export const formatCompactNumber = (n: number) => new Intl.NumberFormat("en-US", {notation:"compact"}).format(n);
