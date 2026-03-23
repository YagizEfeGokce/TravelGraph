function ProfilePage() {
  const trips = [
    "Paris Spring Trip",
    "Rome Weekend Plan",
    "Tokyo Food Tour",
  ];

  const savedPlans = [
    "Summer Europe Route",
    "Winter Japan Budget",
    "Beach Escape Plan",
  ];

  const reviews = [
    "Amazing city experience!",
    "Loved the local restaurants.",
    "Great place for a weekend trip.",
  ];

  return (
    <div className="bg-background min-h-screen pt-24 pb-16 px-6">
      <div className="max-w-screen-xl mx-auto">
        {/* Header */}
        <div className="mb-10">
          <span className="inline-block px-3 py-1 rounded-full bg-primary-fixed text-on-primary-fixed text-[10px] font-bold tracking-widest uppercase mb-3 font-label">
            Your Account
          </span>
          <h1 className="text-5xl font-black font-headline text-on-surface tracking-tight mb-3">
            Profile
          </h1>
          <p className="text-on-surface-variant leading-relaxed">
            View your past trips, saved plans, and reviews.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <ProfileCard
            title="Past Trips"
            items={trips}
            icon="travel_explore"
            accent="primary"
          />
          <ProfileCard
            title="Saved Plans"
            items={savedPlans}
            icon="bookmark"
            accent="secondary"
          />
          <ProfileCard
            title="Your Reviews"
            items={reviews}
            icon="rate_review"
            accent="tertiary"
          />
        </div>
      </div>
    </div>
  );
}

type ProfileCardProps = {
  title: string;
  items: string[];
  icon: string;
  accent: "primary" | "secondary" | "tertiary";
};

function ProfileCard({ title, items, icon, accent }: ProfileCardProps) {
  const accentMap = {
    primary: "text-primary bg-primary/10",
    secondary: "text-secondary bg-secondary/10",
    tertiary: "text-tertiary bg-tertiary/10",
  };

  return (
    <div className="bg-surface-container-lowest rounded-3xl border border-outline-variant/30 shadow-card overflow-hidden">
      <div className="p-6 border-b border-outline-variant/20">
        <div className="flex items-center gap-3 mb-1">
          <div className={`w-10 h-10 rounded-xl flex items-center justify-center ${accentMap[accent]}`}>
            <span className="material-symbols-outlined text-xl">{icon}</span>
          </div>
          <h2 className="text-lg font-black font-headline text-on-surface tracking-tight">
            {title}
          </h2>
        </div>
      </div>
      <ul className="p-4 space-y-2">
        {items.map((item) => (
          <li
            key={item}
            className="flex items-center gap-3 px-3 py-2.5 rounded-xl hover:bg-surface-container-low transition-colors"
          >
            <span className="w-1.5 h-1.5 rounded-full bg-outline flex-shrink-0" />
            <span className="text-sm text-on-surface font-medium">{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default ProfilePage;
