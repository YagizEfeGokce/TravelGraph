import { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { registerUser } from "../api/auth";

function RegisterPage() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");

  async function handleRegister() {
    if (password !== confirmPassword) {
      alert("Passwords do not match.");
      return;
    }

    try {
      await registerUser({ name, email, password });
      alert("Registration successful.");
      navigate("/login");
    } catch (error) {
      console.error("Register failed:", error);
      alert("Register failed. Please try again.");
    }
  }

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "#f8fafc",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        padding: "40px 20px",
      }}
    >
      <div
        style={{
          width: "100%",
          maxWidth: "460px",
          background: "white",
          borderRadius: "20px",
          padding: "36px",
          boxShadow: "0 12px 30px rgba(0,0,0,0.08)",
        }}
      >
        <h1
          style={{
            fontSize: "32px",
            marginBottom: "10px",
            color: "#1f2937",
          }}
        >
          Create Account
        </h1>

        <p
          style={{
            color: "#6b7280",
            marginBottom: "28px",
            lineHeight: 1.5,
          }}
        >
          Join TravelGraph and start organizing your trips more easily.
        </p>

        <div style={{ display: "flex", flexDirection: "column", gap: "16px" }}>
          <div>
            <label
              style={{
                display: "block",
                marginBottom: "8px",
                fontWeight: 600,
                color: "#374151",
              }}
            >
              Full Name
            </label>
            <input
              type="text"
              placeholder="Enter your full name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              style={{
                width: "100%",
                padding: "14px 16px",
                borderRadius: "10px",
                border: "1px solid #d1d5db",
                outline: "none",
                fontSize: "15px",
                boxSizing: "border-box",
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: "block",
                marginBottom: "8px",
                fontWeight: 600,
                color: "#374151",
              }}
            >
              Email
            </label>
            <input
              type="email"
              placeholder="Enter your email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              style={{
                width: "100%",
                padding: "14px 16px",
                borderRadius: "10px",
                border: "1px solid #d1d5db",
                outline: "none",
                fontSize: "15px",
                boxSizing: "border-box",
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: "block",
                marginBottom: "8px",
                fontWeight: 600,
                color: "#374151",
              }}
            >
              Password
            </label>
            <input
              type="password"
              placeholder="Create a password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={{
                width: "100%",
                padding: "14px 16px",
                borderRadius: "10px",
                border: "1px solid #d1d5db",
                outline: "none",
                fontSize: "15px",
                boxSizing: "border-box",
              }}
            />
          </div>

          <div>
            <label
              style={{
                display: "block",
                marginBottom: "8px",
                fontWeight: 600,
                color: "#374151",
              }}
            >
              Confirm Password
            </label>
            <input
              type="password"
              placeholder="Confirm your password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              style={{
                width: "100%",
                padding: "14px 16px",
                borderRadius: "10px",
                border: "1px solid #d1d5db",
                outline: "none",
                fontSize: "15px",
                boxSizing: "border-box",
              }}
            />
          </div>

          <button
            type="button"
            onClick={handleRegister}
            style={{
              marginTop: "8px",
              background: "#14b8a6",
              color: "white",
              border: "none",
              padding: "14px 16px",
              borderRadius: "10px",
              fontSize: "16px",
              fontWeight: 600,
              cursor: "pointer",
            }}
          >
            Register
          </button>
        </div>

        <p
          style={{
            marginTop: "22px",
            textAlign: "center",
            color: "#6b7280",
          }}
        >
          Already have an account?{" "}
          <Link
            to="/login"
            style={{
              color: "#14b8a6",
              textDecoration: "none",
              fontWeight: 600,
            }}
          >
            Login
          </Link>
        </p>
      </div>
    </div>
  );
}

export default RegisterPage;