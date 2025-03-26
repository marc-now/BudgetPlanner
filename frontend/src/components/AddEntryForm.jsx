import { useState, useEffect, useRef } from "react";
import api from "../api";
import "../styles/AddEntryForm.css"

function AddEntryForm({ onEntryAdded }) {
    const [title, setTitle] = useState("");
    const [value, setValue] = useState("");
    const [category, setCategory] = useState("");
    const [categories, setCategories] = useState([]); // Wszystkie kategorie
    const [filteredCategories, setFilteredCategories] = useState([]); // Filtrowana lista kategorii
    const [isDropdownOpen, setIsDropdownOpen] = useState(false);
    const [isIncome, setIsIncome] = useState(false);
    const dropdownRef = useRef(null);

    // Pobranie kategorii z backendu
    useEffect(() => {
        api.get("/api/categories/")
            .then((res) => {
                setCategories(res.data);
                setFilteredCategories(res.data);
            })
            .catch((err) => console.error("Error fetching categories:", err));
    }, []);

    // Obsługa zmiany pola kategorii
    const handleCategoryChange = (e) => {
        const input = e.target.value;
        setCategory(input);

        if (input.length > 0) {
            setFilteredCategories(
                categories.filter((cat) =>
                    cat.name.toLowerCase().includes(input.toLowerCase())
                )
            );
        } else {
            setFilteredCategories(categories); // Jeśli puste, pokaż wszystko
        }

        setIsDropdownOpen(true);
    };

    // Obsługa wyboru kategorii z listy
    const handleCategorySelect = (selectedCategory) => {
        setCategory(selectedCategory);
        setIsDropdownOpen(false);
    };

    // Obsługa zamykania dropdowna, gdy klikniemy poza nim
    useEffect(() => {
        function handleClickOutside(event) {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target)) {
                setIsDropdownOpen(false);
            }
        }

        document.addEventListener("mousedown", handleClickOutside);
        return () => {
            document.removeEventListener("mousedown", handleClickOutside);
        };
    }, []);

    // Obsługa wysłania formularza
    const handleSubmit = (e) => {
        e.preventDefault();
        const adjustedValue = isIncome ? parseFloat(value) : -parseFloat(value);

        // Jeśli kategoria jest nowa, dodaj ją do bazy
        if (!categories.some((cat) => cat.name === category)) {
            api.post("/api/categories/", { name: category })
                .then((res) => {
                    if (res.status === 201) {
                        setCategories([...categories, res.data]); // Dodaj nową kategorię do listy
                    }
                })
                .catch((err) => alert("Error adding category:", err));
        }

        const newEntry = { title, value: adjustedValue, category };

        api.post("/api/entries/", newEntry)
            .then((res) => {
                if (res.status === 201) {
                    onEntryAdded(res.data);
                    setTitle("");
                    setValue("");
                    setCategory("");
                } else {
                    alert("Failed to add the entry.");
                }
            })
            .catch((err) => alert(err));
    };

    return (
        <form className="entry-form-container" onSubmit={handleSubmit}>
            <div className="buttons-container">
                <button
                    type="button"
                    className={`plus-btn${isIncome ? "-active" : ""}`}
                    onClick={() => setIsIncome(true)}
                >
                    +
                </button>
                <button
                    type="button"
                    className={`minus-btn${!isIncome ? "-active" : ""}`}
                    onClick={() => setIsIncome(false)}
                >
                    -
                </button>
            </div>
            <div className="inputs-container">
                <input
                    type="text"
                    id="title"
                    name="title"
                    required
                    onChange={(e) => setTitle(e.target.value)}
                    value={title}
                    placeholder="Title"
                />
                <input
                    type="number"
                    step="0.1"
                    min="0"
                    id="value"
                    name="value"
                    required
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                    placeholder="Amount"
                />

                <div className="category-dropdown" ref={dropdownRef}>
                    <input
                        type="text"
                        id="category"
                        name="category"
                        required
                        value={category}
                        onChange={handleCategoryChange}
                        onFocus={() => {
                            setIsDropdownOpen(true);
                            setFilteredCategories(categories); // Pokaż wszystkie kategorie, gdy aktywne
                        }}
                        placeholder="Category"
                    />
                    {isDropdownOpen && (
                        <ul className="dropdown-list">
                            {filteredCategories.length > 0 ? (
                                filteredCategories.map((cat) => (
                                    <li key={cat.id} onClick={() => handleCategorySelect(cat.name)}>
                                        {cat.name}
                                    </li>
                                ))
                            ) : (
                                <li className="no-results">No matching categories</li>
                            )}
                        </ul>
                    )}
                </div>

                <input type="submit" value="Submit" />
            </div>
        </form>
    );
}

export default AddEntryForm
