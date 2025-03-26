import { useState, useEffect } from "react";
import api from "../api";
import Entry from "../components/Entry";
import "../styles/Home.css"
import Navbar from "../components/Navbar";
import { Tile, TileSlider } from "../components/TileSlider";
import AddEntryForm from "../components/AddEntryForm";


function Home() {
    const [entries, setEntries] = useState([]);

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
        api.delete(`/api/entries/delete/${id}/`)
            .then((res) => {
                if (res.status === 204) {
                    // Delete entry client-side
                    setEntries((prevEntries) => prevEntries.filter((entry) => entry.id !== id));
                } else {
                    alert("Failed to delete entry.");
                }
            })
            .catch((error) => alert(error));
    };

    // Add entry client-side
    const addEntry = (newEntry) => {
        setEntries((prevEntries) => [newEntry, ...prevEntries]);
    };

    let founds = entries.reduce((sum, entry) => sum + parseFloat(entry.value || 0), 0)

    return (
        <div className="home-page-root">
            <div className="header">
                <h1>BUDGET PLANNER</h1>
            </div>
            <div className="top-section-container">
                <section className="top-section-left">
                    <TileSlider>
                        <Tile><p> Total: {founds} </p></Tile>
                        <Tile><h1>Inne konto</h1></Tile>
                    </TileSlider>
                </section>
                <section className="top-section-right">
                    <h1>Tutaj jakieś ładne statystyki/podsumowanie od AI</h1>
                </section>
            </div>
            <div className="low-section-container">
                <div className="low-section-left">
                <h2>Entries</h2>
                    {
                        entries.map((entry) => (
                            <Entry entry={entry} onDelete={() => deleteEntry(entry.id)} key={entry.id} />
                            ))
                            
                    }
                </div>
                <div className="low-section-right">
                    <AddEntryForm onEntryAdded={addEntry} />
                </div>
            </div>
        </div>
    );
}

export default Home;
{/* <>
    <Navbar>

    </Navbar>

    <EntryList>
        {
            entries.map((entry) => (
                <Entry entry={entry} onDelete={() => deleteEntry(entry.id)} key={entry.id} />
                ))
                                
        }
    </EntryList>
</> */}