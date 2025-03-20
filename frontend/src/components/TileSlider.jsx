import { useState } from "react"
import { ArrowBigLeft, ArrowBigRight, Circle, CircleDot } from "lucide-react"
import "../styles/TileSlider.css"

export function Tile({ children }) {
  return <div className="tile">{children}</div>;
}

export function TileSlider({ children }) {
  const [imageIndex, setImageIndex] = useState(0)

  function showNextImage() {
    setImageIndex(index => {
      if (index === children.length - 1) return 0
      return index + 1
    })
  }

  function showPrevImage() {
    setImageIndex(index => {
      if (index === 0) return children.length - 1
      return index - 1
    })
  }

  return (
    <section
      style={{ width: "100%", height: "100%", position: "relative" }}
    >
      <div
        style={{
          width: "100%",
          height: "100%",
          display: "flex",
          overflow: "hidden",
        }}
      >
        {children.map((tile, index) => (
          <div
            aria-hidden={imageIndex !== index}
            className="img-slider-img"
            style={{ translate: `${-100 * imageIndex}%` }}
          >
          {tile}
          </div>
        ))}
      </div>
      <button
        onClick={showPrevImage}
        className="img-slider-btn"
        style={{ left: 0 }}
      >
        <ArrowBigLeft aria-hidden />
      </button>
      <button
        onClick={showNextImage}
        className="img-slider-btn"
        style={{ right: 0 }}
        aria-label="View Next Image"
      >
        <ArrowBigRight aria-hidden />
      </button>
      <div
        style={{
          position: "absolute",
          bottom: ".5rem",
          left: "50%",
          translate: "-50%",
          display: "flex",
          gap: ".25rem",
        }}
      >
        {children.map((_, index) => (
          <button
            key={index}
            className="img-slider-dot-btn"
            aria-label={`View Image ${index + 1}`}
            onClick={() => setImageIndex(index)}
          >
            {index === imageIndex ? (
              <CircleDot aria-hidden />
            ) : (
              <Circle aria-hidden />
            )}
          </button>
        ))}
      </div>
    </section>
  )
}