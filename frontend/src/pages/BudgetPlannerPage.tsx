import { useMemo, useState } from "react";

function BudgetPlannerPage() {
  const [accommodation, setAccommodation] = useState(120);
  const [food, setFood] = useState(80);
  const [transport, setTransport] = useState(50);
  const [activities, setActivities] = useState(70);

  const total = useMemo(() => {
    return accommodation + food + transport + activities;
  }, [accommodation, food, transport, activities]);

  const categories = [
    { label: "Accommodation", value: accommodation, onChange: setAccommodation, icon: "hotel" },
    { label: "Food", value: food, onChange: setFood, icon: "restaurant" },
    { label: "Transport", value: transport, onChange: setTransport, icon: "directions_car" },
    { label: "Activities", value: activities, onChange: setActivities, icon: "local_activity" },
  ];

  return (
    <div className="bg-background min-h-screen pt-24 pb-16 px-6">
      <div className="max-w-2xl mx-auto">
        {/* Header */}
        <div className="mb-10">
          <span className="inline-block px-3 py-1 rounded-full bg-primary-fixed text-on-primary-fixed text-[10px] font-bold tracking-widest uppercase mb-3 font-label">
            Budget Tracker
          </span>
          <h1 className="text-5xl font-black font-headline text-on-surface tracking-tight mb-3">
            Budget Planner
          </h1>
          <p className="text-on-surface-variant leading-relaxed">
            Add your travel expenses item by item and track the total budget.
          </p>
        </div>

        {/* Budget form */}
        <div className="bg-surface-container-lowest rounded-3xl border border-outline-variant/30 shadow-ambient overflow-hidden">
          <div className="p-6 space-y-4">
            {categories.map((cat) => (
              <BudgetField
                key={cat.label}
                label={cat.label}
                icon={cat.icon}
                value={cat.value}
                onChange={cat.onChange}
              />
            ))}
          </div>

          {/* Total */}
          <div className="px-6 py-5 bg-surface-container border-t border-outline-variant/20 flex justify-between items-center">
            <div>
              <p className="text-xs font-bold text-outline uppercase tracking-widest font-label mb-1">
                Total Budget
              </p>
              <h2 className="text-4xl font-black font-headline text-primary">
                €{total}
              </h2>
            </div>
            <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center">
              <span className="material-symbols-outlined text-primary text-3xl">account_balance_wallet</span>
            </div>
          </div>

          <div className="px-6 pb-6">
            <button className="w-full py-4 bg-gradient-to-br from-primary to-primary-container text-on-primary font-bold rounded-2xl shadow-card hover:opacity-90 transition-all">
              Save Budget
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}

type BudgetFieldProps = {
  label: string;
  icon: string;
  value: number;
  onChange: (value: number) => void;
};

function BudgetField({ label, icon, value, onChange }: BudgetFieldProps) {
  return (
    <div className="flex items-center gap-4">
      <div className="w-10 h-10 rounded-xl bg-surface-container flex items-center justify-center flex-shrink-0">
        <span className="material-symbols-outlined text-on-surface-variant text-xl">{icon}</span>
      </div>
      <div className="flex-1">
        <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-1.5 font-label">
          {label}
        </label>
        <div className="relative">
          <span className="absolute left-3 top-1/2 -translate-y-1/2 text-on-surface-variant font-bold text-sm">€</span>
          <input
            type="number"
            min="0"
            value={value}
            onChange={(e) => onChange(Number(e.target.value))}
            className="w-full pl-8 pr-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 font-bold text-sm focus:outline-none focus:border-primary transition-colors"
          />
        </div>
      </div>
    </div>
  );
}

export default BudgetPlannerPage;
