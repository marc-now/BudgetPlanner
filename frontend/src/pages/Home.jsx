import { useState, useEffect } from "react";
import api from "../api";
import Entry from "../components/Entry"

function Home() {
    const [entries, setEntries] = useState([]);
    const [title, setTitle] = useState("");
    const [value, setValue] = useState("");
    const [category, setCategory] = useState("");


    useEffect(() => {
        getEntries();
    }, []);

    const getEntries = () => {
        api
            .get("/api/entries/")
            .then((res) => res.data)
            .then((data) => {
                setEntries(data);
                console.log(data);
            })
            .catch((err) => alert(err));
    };

    const deleteEntry = (id) => {
        api
            .delete(`/api/entries/delete/${id}/`)
            .then((res) => {
                if (res.status === 204) alert("entry deleted!");
                else alert("Failed to delete entry.");
                getEntries();
            })
            .catch((error) => alert(error));
    };

    const createEntry = (e) => {
        e.preventDefault();
        api
            .post("/api/entries/", {title, value, category})
            .then((res) => {
                if (res.status === 201) alert("Entry added!");
                else alert("Failed to add the entry.");
                getEntries();
            })
            .catch((err) => alert(err));
    };

    return (
        <div>
            <div>
                <h2>Entries</h2>
                {entries.map((entry) => (
                    <Entry entry={entry} onDelete={deleteEntry} key={entry.id} />
                ))}
            </div>
            <h2>Add an entry</h2>
            <form onSubmit={createEntry}>
                <label htmlFor="title">Title:</label>
                <br />
                <input
                    type="text"
                    id="title"
                    name="title"
                    required
                    onChange={(e) => setTitle(e.target.value)}
                    value={title}
                />
                <label htmlFor="value">Value:</label>
                <br />
                <textarea
                    id="value"
                    name="value"
                    required
                    value={value}
                    onChange={(e) => setValue(e.target.value)}
                ></textarea>
                <br />
                <textarea
                    id="category"
                    name="category"
                    required
                    value={category}
                    onChange={(e) => setCategory(e.target.value)}
                ></textarea>
                <br />
                <input type="submit" value="Submit"></input>
            </form>
        </div>
    );
}

export default Home