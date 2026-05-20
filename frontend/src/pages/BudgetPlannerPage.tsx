import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import { getBudget, createBudget, updateBudget } from "../api/budget";

function BudgetPlannerPage() {
  const { id: itineraryId } = useParams<{ id: string }>();

  const [totalBudget, setTotalBudget] = useState(0);
  const [currency, setCurrency] = useState("EUR");
  const [hotelBudget, setHotelBudget] = useState(0);
  const [foodBudget, setFoodBudget] = useState(0);
  const [transportBudget, setTransportBudget] = useState(0);
  const [activityBudget, setActivityBudget] = useState(0);

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [existingBudget, setExistingBudget] = useState<any>(null);
  const [saveStatus, setSaveStatus] = useState<"idle" | "saving" | "success" | "error">("idle");

  useEffect(() => {
    if (!itineraryId) return;

    setLoading(true);
    setError(null);
    getBudget(itineraryId)
      .then((data) => {
        setExistingBudget(data);
        setTotalBudget(data.total_budget ?? 0);
        setCurrency(data.currency ?? "EUR");
        setHotelBudget(data.hotel_budget ?? 0);
        setFoodBudget(data.food_budget ?? 0);
        setTransportBudget(data.transport_budget ?? 0);
        setActivityBudget(data.activity_budget ?? 0);
      })
      .catch(() => {
        // Budget may not exist yet — that's fine, we'll create one
        setExistingBudget(null);
      })
      .finally(() => setLoading(false));
  }, [itineraryId]);

  const total = useMemo(() => {
    return hotelBudget + foodBudget + transportBudget + activityBudget;
  }, [hotelBudget, foodBudget, transportBudget, activityBudget]);

  const overBudget = total > totalBudget && totalBudget > 0;

  const categories = [
    { label: "Hotel", value: hotelBudget, onChange: setHotelBudget, icon: "hotel" },
    { label: "Food", value: foodBudget, onChange: setFoodBudget, icon: "restaurant" },
    { label: "Transport", value: transportBudget, onChange: setTransportBudget, icon: "directions_car" },
    { label: "Activities", value: activityBudget, onChange: setActivityBudget, icon: "local_activity" },
  ];

  const handleSave = async () => {
    if (!itineraryId) return;

    setSaveStatus("saving");
    const payload = {
      total_budget: total,
      currency,
      hotel_budget: hotelBudget,
      food_budget: foodBudget,
      transport_budget: transportBudget,
      activity_budget: activityBudget,
    };

    try {
      if (existingBudget) {
        await updateBudget(itineraryId, payload);
      } else {
        await createBudget(itineraryId, payload);
      }
      setExistingBudget(payload);
      setSaveStatus("success");
      setTimeout(() => setSaveStatus("idle"), 3000);
    } catch (err: any) {
      setSaveStatus("error");
      setError(err?.response?.data?.detail || "Failed to save budget.");
      setTimeout(() => setSaveStatus("idle"), 3000);
    }
  };

  if (loading) {
    return (
      <div className="bg-background min-h-screen pt-24 pb-16 px-6 flex items-center justify-center">
        <p className="text-on-surface-variant font-bold">Loading budget...</p>
      </div>
    );
  }

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
                {currency === "EUR" ? "€" : currency === "USD" ? "$" : currency === "GBP" ? "£" : currency} {total}
              </h2>
            </div>
            <div className="w-16 h-16 rounded-2xl bg-primary/10 flex items-center justify-center">
              <span className="material-symbols-outlined text-primary text-3xl">account_balance_wallet</span>
            </div>
          </div>

          {overBudget && (
            <div className="px-6 pb-2">
              <p className="text-sm text-error font-bold">
                Line items exceed total budget by {currency === "EUR" ? "€" : currency === "USD" ? "$" : currency === "GBP" ? "£" : currency} {total - totalBudget}
              </p>
            </div>
          )}

          {saveStatus === "success" && (
            <div className="px-6 pb-2">
              <p className="text-sm text-green-600 font-bold">Budget saved successfully!</p>
            </div>
          )}

          {saveStatus === "error" && error && (
            <div className="px-6 pb-2">
              <p className="text-sm text-error font-bold">{error}</p>
            </div>
          )}

          <div className="px-6 pb-6 pt-2">
            <button
              onClick={handleSave}
              disabled={saveStatus === "saving"}
              className={`w-full py-4 bg-gradient-to-br from-primary to-primary-container text-on-primary font-bold rounded-2xl shadow-card hover:opacity-90 transition-all ${saveStatus === "saving" ? "opacity-60 cursor-not-allowed" : ""}`}
            >
              {saveStatus === "saving" ? "Saving..." : "Save Budget"}
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
            min={0}
            value={value}
            onChange={(e) => onChange(Math.max(0, Number(e.target.value)))}
            className="w-full pl-8 pr-4 py-3 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 font-bold text-sm focus:outline-none focus:border-primary transition-colors"
          />
        </div>
      </div>
    </div>
  );
}

export default BudgetPlannerPage;
