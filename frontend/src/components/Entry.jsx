import React from "react"
import "../styles/Entry.css"

function Entry({entry, onDelete}) {
    const formattedDate = new Date(entry.date).toLocaleDateString("pl-PL")

    return (
        <div className="entry-container">
            <p className="entry-title">{entry.title}</p>
            <p className="entry-content">{entry.category.name}</p>
            <p className="entry-content">{entry.value}</p>
            <p className="entry-date">{formattedDate}</p>
            <button className="delete-button" onClick={() => onDelete(entry.id)}>
                Delete
            </button>
        </div>
    );
}

export default Entry