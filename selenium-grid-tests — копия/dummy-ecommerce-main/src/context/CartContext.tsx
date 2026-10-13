"use client";

import { createContext, useContext, useState, useEffect, useCallback } from "react";
import { Cart } from "@/types";

interface CartContextType {
  cart: Cart;
  cartCount: number;
  addToCart: (productId: string, quantity?: number) => Promise<void>;
  removeFromCart: (cartItemId: string) => Promise<void>;
  updateQuantity: (cartItemId: string, quantity: number) => Promise<void>;
  refreshCart: () => Promise<void>;
}

const CartContext = createContext<CartContextType | null>(null);

export function CartProvider({ children }: { children: React.ReactNode }) {
  const [cart, setCart] = useState<Cart>({ items: [], total: 0 });

  const refreshCart = useCallback(async () => {
    const res = await fetch("/api/cart");
    const data = await res.json();
    setCart(data);
  }, []);

  useEffect(() => {
    refreshCart();
  }, [refreshCart]);

  const addToCart = async (productId: string, quantity: number = 1) => {
    const res = await fetch("/api/cart", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ productId, quantity }),
    });
    const data = await res.json();
    setCart(data);
  };

  const removeFromCart = async (cartItemId: string) => {
    const res = await fetch(`/api/cart/${cartItemId}`, {
      method: "DELETE",
    });
    const data = await res.json();
    setCart(data);
  };

  const updateQuantity = async (cartItemId: string, quantity: number) => {
    const res = await fetch(`/api/cart/${cartItemId}`, {
      method: "PATCH",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ quantity }),
    });
    const data = await res.json();
    setCart(data);
  };

  const cartCount = cart.items.reduce((sum, item) => sum + item.quantity, 0);

  return (
    <CartContext.Provider
      value={{ cart, cartCount, addToCart, removeFromCart, updateQuantity, refreshCart }}
    >
      {children}
    </CartContext.Provider>
  );
}

export function useCart() {
  const context = useContext(CartContext);
  if (!context) {
    throw new Error("useCart must be used within a CartProvider");
  }
  return context;
}
