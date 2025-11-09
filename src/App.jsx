import React from "react";
import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./Header";
import Home from "./Home";       // your map page wrapper
import About from "./About";     // new about page
import "./Header.css";

export default function App() {
  return (
    <BrowserRouter>
      <Header />
      <Routes>
        <Route path="/" element={<Home />} />     {/* map & app content */}
        <Route path="/about" element={<About />} />
      </Routes>
    </BrowserRouter>
  );
}
