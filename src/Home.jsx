import React from "react";
import MapFrame from "./MapFrame";
import FactsBar from "./FactsBar";
import CountryYearQuery from "./CountryYearQuery";

export default function Home() {
  return (
    <>
      <CountryYearQuery />
      <MapFrame />
    </>
  );
}
