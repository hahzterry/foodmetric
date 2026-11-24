export interface ProductItem {
  rank_overall: number;
  rank_in_category: number;
  product_id: string;
  product_name: string;
  category_slug: string;
  creator_handle?: string;
  creator_name?: string;
  creator_followers?: string;
  video_url?: string;
  video_views?: number;
  video_likes?: number;
  current_price: number;
  image_url: string;
  affiliate_url: string;
  product_rating: number;
  review_count: number;
  shop_id: string;
  shop_name: string;
  is_shop_official: boolean;
  historical_sold: number;
  estimated_daily_units: number;
  estimated_daily_gmv: number;
  anomaly_flag: boolean;
}

export interface CategoryInfo {
  name: string;
  keywords: string[];
  base_volume: number;
}

export interface BentoTopCategory {
  slug: string;
  name: string;
  gmv: number;
}

export interface BentoViralHook {
  hook_text: string;
  recommended_sound: string;
  views_benchmark: string;
}

export interface BentoKPIs {
  top_gmv_product: ProductItem | null;
  fastest_growth_product: ProductItem | null;
  top_category: BentoTopCategory;
  top_viral_hook: BentoViralHook;
}

export interface DashboardMetadata {
  last_updated: string;
  snapshot_date: string;
  total_products_indexed: number;
  total_estimated_daily_gmv: number;
  total_estimated_daily_units: number;
}

export interface DashboardData {
  metadata: DashboardMetadata;
  categories: Record<string, CategoryInfo>;
  bento_kpis: BentoKPIs;
  leaderboard: ProductItem[];
}

export type CategoryFilterId = "all" | "under-10" | "chips-crackers" | "jerky-protein" | "candy-sweets" | "beverages" | "other-snacks";
