// About.jsx
import React from "react";
import { useNavigate } from "react-router-dom";
import "./Header.css"; // reuse your styles or add more
import Karl from "../src/assets/KARL.jpg";
import Achebe from "../src/assets/ACHEBE.jpg";
import Isaac from "../src/assets/ISAAC.jpg";
import Daniel from "../src/assets/DANIEL.jpg";
import Viho from "../src/assets/VIHO.jpg";

const team = [
    { name: "Karl Andres", img: Karl },
    { name: "Achebe Culpepper", img: Achebe },
    { name: "Isaac Doyle", img: Isaac },
    { name: "Daniel Hyman", img: Daniel },
    { name: "Viho Huang", img: Viho }
  ];


export default function About() {
  const navigate = useNavigate();

  const team = [
    { name: "Karl Andres", img: Karl },
    { name: "Achebe Culpepper", img: Achebe },
    { name: "Isaac Doyle", img: Isaac },
    { name: "Daniel Hyman", img: Daniel },
    { name: "Viho Huang", img: Viho }
  ];

  return (
    <div className="container" style={{ padding: "30px" }}>
      <h1 style={{ textAlign: "center", marginBottom: "20px" }}>
        Meet the Leaf Watch Team 🍃
      </h1>

      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(5, 1fr)",
          gap: "20px",
          marginBottom: "30px"
        }}
      >
        {team.map((person) => (
          <div
            key={person.name}
            style={{
              textAlign: "center",
              padding: "10px",
              background: "#fff",
              borderRadius: "10px",
              boxShadow: "0 2px 8px rgba(0,0,0,0.1)"
            }}
          >
            <img
              src={person.img}
              alt={person.name}
              style={{
                width: "100%",
                borderRadius: "10px",
                marginBottom: "10px"
              }}
            />
            <h3>{person.name}</h3>
          </div>
        ))}
      </div>

      <button
        className="btn"
        style={{ padding: "10px 18px", display: "block", margin: "0 auto" }}
        onClick={() => navigate(-1)}
      >
        ← Back
      </button>
    </div>
  );
}
