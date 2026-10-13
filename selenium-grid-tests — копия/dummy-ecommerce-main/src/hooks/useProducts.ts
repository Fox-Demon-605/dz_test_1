"use client";

import { useState, useEffect } from "react";
import { Product } from "@/types";

export function useProducts(search: string, category: string, sort: string) {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const params = new URLSearchParams();
    if (search) params.set("search", search);
    if (category) params.set("category", category);
    if (sort) params.set("sort", sort);

    setLoading(true);
    fetch(`/api/products?${params.toString()}`)
      .then((res) => res.json())
      .then((data) => {
        setProducts(data.products);
        setError(null);
      })
      .catch((err) => {
        setError(err.message);
      })
      .finally(() => {
        setLoading(false);
      });
  }, [search, category, sort]);

  return { products, loading, error };
}
