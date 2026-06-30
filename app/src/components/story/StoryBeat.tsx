import type { ReactNode } from "react";
import type { Beat } from "../../lib/tour";

type StoryBeatProps = {
  beat: Beat;
  index: number;
  total: number;
  children?: ReactNode;
};

// One scroll beat: one claim, one caveat, one optional in-card control, one
// action hint. The map (behind/above the rail) is the actual evidence surface.
export function StoryBeat({ beat, index, total, children }: StoryBeatProps) {
  return (
    <div className="beat">
      <p className="beat__eyebrow">
        Beat {index + 1} of {total} &middot; {beat.short}
      </p>
      <h2 className="beat__title">{beat.title}</h2>
      <p className="beat__claim">{beat.claim}</p>
      <p className="beat__caveat">{beat.caveat}</p>
      {children && <div className="beat__extra">{children}</div>}
      {beat.source && <p className="beat__source">Evidence: {beat.source}</p>}
      <p className="beat__action">{beat.action}</p>
    </div>
  );
}
