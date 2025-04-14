import React, {useState } from "react"
import { ChevronDown, Trash2, Pencil } from 'lucide-react';
import "../styles/Entry.css"

function Entry({entry, onDelete}) {
    const [expanded, setExpanded] = useState(false)
    const formattedDate = new Date(entry.date).toLocaleDateString("pl-PL")

    function toggleExpanded() {
        setExpanded(!expanded)
    }

    return (
        <div className={`entry-container`}>
            <div className="entry-heading"> 
                <p className="entry-title">{entry.title}</p>
                <p className="entry-content">{entry.category.name}</p>
                <p className="entry-content">{entry.value}</p> 
                <button className="entry-button" onClick={toggleExpanded}>
                    <ChevronDown />
                </button>           
            </div>
            <div className={`entry-details ${expanded ? "expanded" : ""}`}>
                <div className="inner">
                    <p className="entry-account">konto</p>
                    <p className="entry-subcategory">podkategoria</p>
                    <p className="entry-date">{formattedDate}</p>
                    <button className="entry-button" onClick={() => onDelete(entry.id)}>
                        <Trash2 />
                    </button>
                    <p className="entry-description">
                        Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quis impedit et 
                        doloribus aliquid earum, a enim nulla voluptate commodi dolore cupiditate 
                        iusto nisi, aspernatur facilis porro. Dolor rem accusamus ipsam.Lorem, ipsum dolor sit amet consectetur adipisicing elit. Quis impedit et 
                        doloribus aliquid earum, a enim nulla voluptate commodi dolore cupiditate 
                        iusto nisi, aspernatur facilis porro. Dolor rem accusamus ipsam.
                    </p>
                    <button className="entry-button"><Pencil /></button>
                </div>
            </div>
        </div>
    );
}

export default Entry