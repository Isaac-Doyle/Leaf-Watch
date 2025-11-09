import React from "react";
import "./Header.css";

export default function Header() {
  return (
    <header className="site-header">
      <div className="container nav">
        <a href="/" className="brand" aria-label="Leaf Watch home">
          <span className="brand-text">Leaf Watch 🍃</span>
        </a>
        <nav className="nav-actions" aria-label="Primary">
          <a className="btn btn-about" href="/about">About</a>
        </nav>
      </div>
    </header>
  );
}
