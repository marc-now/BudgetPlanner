import React from "react"

function Entry({entry, onDelete}) {
    const formattedDate = new Date(entry.date).toLocaleDateString("pl-PL")

    return (
        <div className="entry-container">
            <p className="entry-title">{entry.title}</p>
            <p className="entry-category">{entry.category.name}</p>
            <p className="entry-value">{entry.value}</p>
            <p className="entry-date">{formattedDate}</p>
            <button className="delete-button" onClick={() => onDelete(entry.id)}>
                Delete
            </button>
        </div>
    );
}

export default Entry