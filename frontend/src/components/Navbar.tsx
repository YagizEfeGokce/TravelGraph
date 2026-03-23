import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";

function Navbar() {
  const { user, logout } = useAuth();
  const location = useLocation();

  const isActive = (path: string) =>
    location.pathname === path || location.pathname.startsWith(path + "/");

  return (
    <nav className="fixed top-0 w-full z-50 glass-nav border-b border-outline-variant/30 shadow-ambient">
      <div className="flex justify-between items-center w-full px-6 py-4 max-w-screen-2xl mx-auto">
        <div className="flex items-center gap-8">
          <Link
            to="/"
            className="text-2xl font-black tracking-tighter text-primary font-headline"
          >
            TravelGraph
          </Link>
          <div className="hidden md:flex items-center gap-6">
            <Link
              to="/"
              className={`font-headline font-medium text-sm tracking-tight transition-colors ${
                isActive("/") && location.pathname === "/"
                  ? "text-primary border-b-2 border-primary pb-1 font-bold"
                  : "text-on-surface-variant hover:text-primary"
              }`}
            >
              Home
            </Link>
            <Link
              to="/explore"
              className={`font-headline font-medium text-sm tracking-tight transition-colors ${
                isActive("/explore") || isActive("/destinations")
                  ? "text-primary border-b-2 border-primary pb-1 font-bold"
                  : "text-on-surface-variant hover:text-primary"
              }`}
            >
              Explore
            </Link>
            <Link
              to="/planner"
              className={`font-headline font-medium text-sm tracking-tight transition-colors ${
                isActive("/planner")
                  ? "text-primary border-b-2 border-primary pb-1 font-bold"
                  : "text-on-surface-variant hover:text-primary"
              }`}
            >
              Planner
            </Link>
            <Link
              to="/festivals"
              className={`font-headline font-medium text-sm tracking-tight transition-colors ${
                isActive("/festivals")
                  ? "text-primary border-b-2 border-primary pb-1 font-bold"
                  : "text-on-surface-variant hover:text-primary"
              }`}
            >
              Festivals
            </Link>
          </div>
        </div>

        <div className="flex items-center gap-3">
          {user ? (
            <>
              <span className="hidden sm:block text-sm text-on-surface-variant font-medium">
                {user.name}
              </span>
              <Link
                to="/profile"
                className="p-2 hover:bg-surface-container-low rounded-lg transition-all"
              >
                <span className="material-symbols-outlined text-on-surface-variant">
                  account_circle
                </span>
              </Link>
              <button
                onClick={logout}
                className="px-4 py-2 text-sm font-bold text-error border border-error/30 rounded-lg hover:bg-error/10 transition-all"
              >
                Logout
              </button>
            </>
          ) : (
            <>
              <Link
                to="/login"
                className="px-4 py-2 text-sm font-bold text-primary border border-primary/30 rounded-lg hover:bg-surface-container-low transition-all"
              >
                Login
              </Link>
              <Link
                to="/register"
                className="px-4 py-2 text-sm font-bold text-on-primary bg-gradient-to-br from-primary to-primary-container rounded-lg shadow-card hover:opacity-90 transition-all"
              >
                Register
              </Link>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

export default Navbar;
