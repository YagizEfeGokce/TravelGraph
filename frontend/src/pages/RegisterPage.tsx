import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../api/auth";
import { useAuth } from "../contexts/AuthContext";

function RegisterPage() {
  const navigate = useNavigate();
  const { login } = useAuth();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleRegister() {
    if (!name || !email || !password) {
      setError("Please fill in all fields.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }
    if (password.length < 8) {
      setError("Password must be at least 8 characters.");
      return;
    }
    setLoading(true);
    setError("");
    try {
      const data = await registerUser({ name, email, password });
      login(data.access_token, data.user);
      navigate("/");
    } catch (err: any) {
      const detail = err?.response?.data?.detail;
      setError(detail || "Registration failed. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen bg-background flex items-center justify-center px-6 py-20">
      <div className="w-full max-w-md">
        {/* Card */}
        <div className="bg-surface-container-lowest rounded-3xl border border-outline-variant/30 shadow-ambient overflow-hidden">
          {/* Top accent */}
          <div className="h-1.5 bg-gradient-to-r from-primary to-primary-container" />

          <div className="p-8 md:p-10">
            <div className="mb-8">
              <Link to="/" className="text-xl font-black text-primary font-headline tracking-tighter mb-6 block">
                TravelGraph
              </Link>
              <h1 className="text-3xl font-black font-headline text-on-surface tracking-tight mb-2">
                Create Account
              </h1>
              <p className="text-on-surface-variant leading-relaxed">
                Join TravelGraph and start organizing your trips.
              </p>
            </div>

            <div className="space-y-4">
              <div>
                <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                  Full Name
                </label>
                <input
                  type="text"
                  placeholder="Enter your full name"
                  value={name}
                  onChange={(e) => setName(e.target.value)}
                  className="w-full px-4 py-3.5 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm focus:outline-none focus:border-primary transition-colors placeholder:text-outline"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                  Email
                </label>
                <input
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  className="w-full px-4 py-3.5 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm focus:outline-none focus:border-primary transition-colors placeholder:text-outline"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                  Password
                </label>
                <input
                  type="password"
                  placeholder="Min. 8 characters"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  className="w-full px-4 py-3.5 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm focus:outline-none focus:border-primary transition-colors placeholder:text-outline"
                />
              </div>

              <div>
                <label className="block text-xs font-bold text-outline uppercase tracking-widest mb-2 font-label">
                  Confirm Password
                </label>
                <input
                  type="password"
                  placeholder="Confirm your password"
                  value={confirmPassword}
                  onChange={(e) => setConfirmPassword(e.target.value)}
                  onKeyDown={(e) => e.key === "Enter" && handleRegister()}
                  className="w-full px-4 py-3.5 rounded-xl bg-surface-container text-on-surface border border-outline-variant/30 text-sm focus:outline-none focus:border-primary transition-colors placeholder:text-outline"
                />
              </div>

              {error && (
                <div className="bg-error-container text-on-error-container px-4 py-3 rounded-xl text-sm">
                  {error}
                </div>
              )}

              <button
                type="button"
                onClick={handleRegister}
                disabled={loading}
                className="w-full py-4 mt-2 bg-gradient-to-br from-primary to-primary-container text-on-primary font-bold rounded-xl shadow-card hover:opacity-90 transition-all disabled:opacity-60 disabled:cursor-not-allowed"
              >
                {loading ? "Creating account..." : "Register"}
              </button>
            </div>

            <p className="mt-6 text-center text-sm text-on-surface-variant">
              Already have an account?{" "}
              <Link to="/login" className="text-primary font-bold hover:underline">
                Login
              </Link>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RegisterPage;
