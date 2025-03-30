import React, { useState, useEffect } from "react";
import axios from "axios";

const Search = () => {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [debouncedQuery, setDebouncedQuery] = useState("");

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedQuery(query);
    }, 300);
    return () => clearTimeout(handler);
  }, [query]);

  useEffect(() => {
    console.log("Updated Results:", results);
  }, [results]);

  const handleInputChange = (e) => {
    setQuery(e.target.value);
  };

  const handleSearch = async () => {
    if (!debouncedQuery.trim()) return;
    setLoading(true);

    try {
      const { data } = await axios.get("http://127.0.0.1:5000/search", {
        params: { query: debouncedQuery },
      });

      console.log("API Response:", data);

      setResults(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Error fetching data:", error);
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      {/* Navbar */}
      <nav className="navbar">
        <h2>RandomSeed42</h2>
      </nav>

      {/* Main Content */}
      <section className="main-content">
        {/* Search Box (Now Above the List) */}
        <div className="search-box">
          <input
            type="text"
            value={query}
            onChange={handleInputChange}
            placeholder="Search here..."
          />
          <button className="search-btn" onClick={handleSearch} disabled={loading}>
            {loading ? "Searching..." : "Search"}
          </button>
        </div>

        {/* Results List */}
        <div className="results-container">
          {loading && <p>Loading...</p>}
          {!loading && results.length > 0 ? (
            <ol className="results-list">
              {results.map((item, index) => (
                <li key={index}>
                  <strong>{item.Product_Name}</strong>
                </li>
              ))}
            </ol>
          ) : (
            !loading && query && <p className="no-results">No results found.</p>
          )}
        </div>
      </section>
    </>
  );
};

export default Search;
