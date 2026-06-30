import type { Beat } from "../../lib/tour";

type BeatProgressProps = {
  beats: Beat[];
  index: number;
  onJump: (i: number) => void;
};

// Doubles as a compact navigation rail (vertical ticks on desktop, dots on
// mobile). Every tick is a real button, so keyboard users can jump beats.
export function BeatProgress({ beats, index, onJump }: BeatProgressProps) {
  return (
    <ol className="beat-progress" aria-label="Story progress">
      {beats.map((b, i) => (
        <li key={b.id}>
          <button
            type="button"
            className="beat-progress__tick"
            aria-current={i === index ? "step" : undefined}
            data-done={i < index ? "true" : "false"}
            onClick={() => onJump(i)}
          >
            <span className="beat-progress__dot" aria-hidden="true" />
            <span className="beat-progress__label">{b.short}</span>
          </button>
        </li>
      ))}
    </ol>
  );
}
