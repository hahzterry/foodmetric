"use client";

import React, { useState, useEffect, useMemo, useCallback } from "react";
import { Navbar } from "@/components/Navbar";
import { BentoGrid } from "@/components/BentoGrid";
import { CategoryTabs } from "@/components/CategoryTabs";
import { LeaderboardTable } from "@/components/LeaderboardTable";
import { VideoModal } from "@/components/VideoModal";
import { RandomSnackModal } from "@/components/RandomSnackModal";
import { DailyTarotModal } from "@/components/DailyTarotModal";
import { StickyMobileBar } from "@/components/StickyMobileBar";
import { DashboardData, CategoryFilterId, ProductItem } from "@/types";
import { formatNumber } from "@/lib/utils";
import { Flame, Package, Tag, Share2, Check, AlertCircle } from "lucide-react";
import initialData from "@/public/data/leaderboard_latest.json";

// FIXED: $5.00 = 500 cents. (Previously 50000 = $500.00, which mismatched the UI label)
const UNDER_5_PRICE_THRESHOLD = 500; 
const TIKTOK_HANDLE = "@foodlenlut";
const TIKTOK_URL = `https://www.tiktok.com/${TIKTOK_HANDLE}`;

export default function HomePage() {
  const [data, setData] = useState<DashboardData>(
    initialData as unknown as DashboardData
  );
  const [searchQuery, setSearchQuery] = useState<string>("");
  const [debouncedQuery, setDebouncedQuery] = useState<string>("");
  const [activeCategory, setActiveCategory] =
    useState<CategoryFilterId>("all");
  const [selectedProduct, setSelectedProduct] =
    useState<ProductItem | null>(null);
  const [isRandomModalOpen, setIsRandomModalOpen] = useState<boolean>(false);
  const [isTarotModalOpen, setIsTarotModalOpen] = useState<boolean>(false);
  const [shareCopied, setShareCopied] = useState<boolean>(false);
  const [fetchError, setFetchError] = useState<string | null>(null);

  // Debounce search input to prevent excessive re-filtering
  useEffect(() => {
    const timer = setTimeout(() => setDebouncedQuery(searchQuery), 300);
    return () => clearTimeout(timer);
  }, [searchQuery]);

  // Unified product selection handler (accepts ProductItem or product_id string)
  const handleSelectProduct = useCallback(
    (productOrId: ProductItem | string | null) => {
      setIsRandomModalOpen(false);
      setIsTarotModalOpen(false);

      if (typeof productOrId === "string") {
        const found = data?.leaderboard?.find(
          (p) => p.product_id === productOrId
        );
        setSelectedProduct(found || null);
      } else {
        setSelectedProduct(productOrId);
      }
    },
    [data]
  );

  const handleOpenRandomSnack = useCallback(() => {
    setSelectedProduct(null);
    setIsTarotModalOpen(false);
    setIsRandomModalOpen(true);
  }, []);

  const handleOpenTarot = useCallback(() => {
    setSelectedProduct(null);
    setIsRandomModalOpen(false);
    setIsTarotModalOpen(true);
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    const fetchData = async () => {
      try {
        const res = await fetch("/data/leaderboard_latest.json", {
          cache: "no-store",
          signal: controller.signal,
        });
        if (res.ok) {
          const json: DashboardData = await res.json();
          setData(json);
          setFetchError(null);
        } else {
          setFetchError("Failed to load live data. Showing cached version.");
        }
      } catch (err) {
        if ((err as Error).name !== "AbortError") {
          setFetchError("Network error. Showing cached version.");
        }
      }
    };
    fetchData();
    return () => controller.abort();
  }, []);

  const categoryCounts = useMemo<Record<CategoryFilterId, number>>(() => {
    const counts: Record<CategoryFilterId, number> = {
      all: 0,
      "under-50k": 0, // Note: The ID is "under-50k" but logic now checks under $5
      "banh-trang": 0,
      "kho-cac-loai": 0,
      "do-uong": 0,
      "an-vat-khac": 0,
      "com-chay": 0,
    };

    if (!data?.leaderboard) return counts;

    counts.all = data.leaderboard.length;
    for (const item of data.leaderboard) {
      // Count under-$5 items (using the corrected threshold)
      if (item.current_price <= UNDER_5_PRICE_THRESHOLD) {
        counts["under-50k"]++;
      }
      // Count by specific category
      if (item.category_slug in counts) {
        counts[item.category_slug as CategoryFilterId]++;
      }
    }
    return counts;
  }, [data]);

  const filteredProducts = useMemo<ProductItem[]>(() => {
    if (!data?.leaderboard) return [];

    const query = debouncedQuery.toLowerCase().trim();

    return data.leaderboard.filter((item) => {
      // Category filter
      if (activeCategory === "under-50k") {
        if (item.current_price > UNDER_5_PRICE_THRESHOLD) return false;
      } else if (
        activeCategory !== "all" &&
        item.category_slug !== activeCategory
      ) {
        return false;
      }

      // Search filter
      if (query) {
        return (
          item.product_name.toLowerCase().includes(query) ||
          item.shop_name.toLowerCase().includes(query) ||
          item.category_slug.toLowerCase().includes(query)
        );
      }

      return true;
    });
  }, [data, activeCategory, debouncedQuery]);

  const categoryNames = useMemo<Record<string, string>>(() => {
    if (!data?.categories) return {};
    const map: Record<string, string> = {};
    for (const [slug, info] of Object.entries(data.categories)) {
      map[slug] = info.name;
    }
    return map;
  }, [data]);

  const under5Count = useMemo(() => {
    if (!data?.leaderboard) return 0;
    return data.leaderboard.filter(
      (p) => p.current_price <= UNDER_5_PRICE_THRESHOLD
    ).length;
  }, [data]);

  const handleShareWeb = useCallback(async () => {
    if (typeof window === "undefined") return;

    const shareData = {
      title: "FoodMetric — Viral TikTok Snack Leaderboard",
      text: "Check out the hottest viral snacks trending on TikTok Shop right now!",
      url: window.location.href,
    };

    // Try native share first (works great on mobile)
    if (navigator.share) {
      try {
        await navigator.share(shareData);
        return;
      } catch {
        // User cancelled or share failed — fall through to clipboard
      }
    }

    // Fallback to clipboard
    if (navigator.clipboard) {
      try {
        await navigator.clipboard.writeText(window.location.href);
        setShareCopied(true);
        setTimeout(() => setShareCopied(false), 2500);
      } catch {
        // Clipboard write failed silently
      }
    }
  }, []);

  return (
    <div className="min-h-screen bg-[#F8FAFC] text-slate-900 flex flex-col selection:bg-orange-100 selection:text-orange-900 pb-16 sm:pb-0">
      <Navbar
        searchQuery={searchQuery}
        onSearchChange={setSearchQuery}
        lastUpdated={data?.metadata.last_updated}
        totalProducts={data?.metadata.total_products_indexed}
        onOpenRandomSnack={handleOpenRandomSnack}
        onOpenTarot={handleOpenTarot}
      />

      <main className="mx-auto flex-1 w-full max-w-container px-4 py-6 sm:px-6 sm:py-8 space-y-6 pb-24 md:pb-12">
        {/* Fetch Error Banner */}
        {fetchError && (
          <div className="flex items-center gap-2 rounded-xl border border-amber-200 bg-amber-50 px-4 py-3 text-sm text-amber-800">
            <AlertCircle className="h-4 w-4 shrink-0" />
            <span>{fetchError}</span>
          </div>
        )}

        {/* Hero Section */}
        <section className="relative overflow-hidden rounded-3xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs">
          <div className="relative z-10 flex flex-col gap-6 lg:flex-row lg:items-center lg:justify-between">
            <div>
              <div className="flex flex-wrap items-center gap-2">
                <span className="inline-flex items-center gap-1.5 rounded-full border border-orange-200 bg-orange-50 px-3 py-1 text-xs font-bold text-orange-700">
                  <Flame className="h-3.5 w-3.5 text-orange-600" />
                  Viral TikTok Shop Snacks
                </span>
                <button
                  type="button"
                  onClick={handleOpenTarot}
                  className="inline-flex items-center gap-1.5 rounded-full border border-purple-200 bg-purple-50/90 px-3 py-1 text-xs font-bold text-purple-700 shadow-xs hover:bg-purple-100 transition-all active:scale-95 cursor-pointer"
                >
                  🔮 Today&apos;s Tarot Pick
                </button>
                <button
                  type="button"
                  onClick={handleOpenRandomSnack}
                  className="inline-flex items-center gap-1.5 rounded-full border border-orange-200 bg-orange-50/80 px-3 py-1 text-xs font-bold text-orange-800 shadow-xs hover:bg-orange-100 transition-all active:scale-95 cursor-pointer"
                >
                  🎲 What Should I Eat? (Random)
                </button>
              </div>

              <h1 className="mt-3 text-2xl sm:text-4xl font-extrabold tracking-tight text-slate-900">
                Hunt Down the Viral Snacks Taking Over TikTok Shop
              </h1>
              <p className="mt-2 max-w-2xl text-xs sm:text-sm text-slate-600">
                Break down the top-selling snacks, million-view videos, and the
                best deals — all in one place, updated daily.
              </p>
            </div>

            {/* Friendly Macro Counters */}
            <div className="grid grid-cols-2 gap-3 sm:flex sm:items-center sm:gap-4">
              <div className="rounded-2xl border border-slate-200 bg-slate-50/80 p-4">
                <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
                  <Package className="h-3.5 w-3.5 text-orange-600" />
                  <span>Orders / Day</span>
                </div>
                <div className="mt-1 text-lg sm:text-2xl font-extrabold font-lexend text-emerald-700">
                  +{formatNumber(data.metadata.total_estimated_daily_units)}
                </div>
                <div className="text-[10px] text-slate-400">
                  From the hottest items
                </div>
              </div>

              <div className="rounded-2xl border border-slate-200 bg-slate-50/80 p-4">
                <div className="flex items-center gap-1.5 text-xs text-slate-500 font-medium">
                  <Tag className="h-3.5 w-3.5 text-orange-600" />
                  <span>Under $5 Picks</span>
                </div>
                <div className="mt-1 text-lg sm:text-2xl font-extrabold font-lexend text-slate-900">
                  {under5Count} Items
                </div>
                <div className="text-[10px] text-slate-400">
                  Budget-friendly &amp; tasty
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* Traffic Area: Voucher Hub + Snack Battle + 2 Featured Cards */}
        <BentoGrid
          kpis={data.bento_kpis}
          onSelectProduct={handleSelectProduct}
        />

        {/* Community & TikTok Creator Banner */}
        <section className="rounded-3xl border border-orange-200 bg-gradient-to-r from-orange-50/60 via-white to-amber-50/60 p-5 sm:p-6 shadow-xs">
          <div className="flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
            <div className="space-y-1 max-w-2xl">
              <h2 className="text-base sm:text-lg font-bold text-slate-900 flex items-center gap-2">
                <span>🔥 Ride With the Food Lén Lút Crew</span>
              </h2>
              <p className="text-xs sm:text-sm text-slate-600">
                Love snacks or on the hunt for viral TikTok Shop finds? Follow{" "}
                <strong>{TIKTOK_HANDLE}</strong> on TikTok for real reviews,
                exclusive $5–$15 vouchers, and new drops every day!
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-2.5 shrink-0">
              <a
                href={TIKTOK_URL}
                target="_blank"
                rel="noopener noreferrer"
                className="inline-flex items-center gap-2 rounded-xl bg-orange-600 px-4 py-2.5 text-xs sm:text-sm font-bold text-white shadow-xs hover:bg-orange-700 transition-all active:scale-95"
              >
                Follow {TIKTOK_HANDLE} ↗
              </a>
              <button
                type="button"
                onClick={handleShareWeb}
                className="inline-flex items-center gap-1.5 rounded-xl border border-slate-200 bg-white px-3.5 py-2.5 text-xs sm:text-sm font-bold text-slate-700 shadow-xs hover:bg-slate-50 transition-all active:scale-95"
              >
                {shareCopied ? (
                  <>
                    <Check className="h-4 w-4 text-emerald-600" />
                    <span>Link copied!</span>
                  </>
                ) : (
                  <>
                    <Share2 className="h-4 w-4 text-slate-500" />
                    <span>Share With Friends</span>
                  </>
                )}
              </button>
            </div>
          </div>
        </section>

        {/* Category Tabs Filter */}
        <div className="pt-2">
          <CategoryTabs
            activeCategory={activeCategory}
            onSelectCategory={setActiveCategory}
            categoryCounts={categoryCounts}
          />
        </div>

        {/* Master Leaderboard Table */}
        <LeaderboardTable
          products={filteredProducts}
          categoryNames={categoryNames}
          onSelectProduct={handleSelectProduct}
        />
      </main>

      {/* Video Popup Modal */}
      <VideoModal
        product={selectedProduct}
        onClose={() => setSelectedProduct(null)}
      />

      {/* Random Snack Modal */}
      <RandomSnackModal
        isOpen={isRandomModalOpen}
        onClose={() => setIsRandomModalOpen(false)}
        products={data?.leaderboard || []}
        onSelectProduct={handleSelectProduct}
      />

      {/* Daily Tarot Modal */}
      <DailyTarotModal
        isOpen={isTarotModalOpen}
        onClose={() => setIsTarotModalOpen(false)}
        onSelectProductById={handleSelectProduct} // Now accepts ID directly via unified handler
      />

      <footer className="mt-12 border-t border-slate-200 bg-white py-6 text-center text-xs text-slate-500">
        <div className="mx-auto max-w-container px-4 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p>
            FoodMetric © 2026 — Your go-to hub for viral snack finds &amp;
            TikTok Shop deals.
          </p>
          <div className="flex items-center gap-4 text-[11px] text-slate-400">
            <span>Powered by the Food Lén Lút community</span>
          </div>
        </div>
      </footer>

      {/* Sticky Mobile Action Bar */}
      <StickyMobileBar
        onOpenRandomSnack={handleOpenRandomSnack}
        onOpenTarot={handleOpenTarot}
      />
    </div>
  );
}
