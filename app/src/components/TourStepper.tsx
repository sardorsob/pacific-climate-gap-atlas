import { ChevronLeft, ChevronRight, X } from "lucide-react";

export type TourStep = {
  title: string;
  body: string;
  source: string;
};

type TourStepperProps = {
  steps: TourStep[];
  index: number;
  onStep: (index: number) => void;
  onClose: () => void;
};

export function TourStepper({ steps, index, onStep, onClose }: TourStepperProps) {
  const step = steps[index];
  const isFirst = index === 0;
  const isLast = index === steps.length - 1;

  return (
    <section className="tour" role="region" aria-label="Guided tour">
      <div className="tour__head">
        <span className="tour__count">
          Tour - {index + 1}/{steps.length}
        </span>
        <button type="button" className="icon-btn" aria-label="Exit tour" onClick={onClose}>
          <X aria-hidden="true" size={16} />
        </button>
      </div>
      <h2 className="tour__title">{step.title}</h2>
      <p className="tour__body">{step.body}</p>
      <p className="tour__source">Evidence: {step.source}</p>
      <div className="tour__nav">
        <button type="button" className="tour__btn" disabled={isFirst} onClick={() => onStep(index - 1)}>
          <ChevronLeft aria-hidden="true" size={16} /> Back
        </button>
        {isLast ? (
          <button type="button" className="tour__btn tour__btn--primary" onClick={onClose}>
            Finish
          </button>
        ) : (
          <button type="button" className="tour__btn tour__btn--primary" onClick={() => onStep(index + 1)}>
            Next <ChevronRight aria-hidden="true" size={16} />
          </button>
        )}
      </div>
    </section>
  );
}
