import { Link } from "react-router-dom";

const isLoggedIn = false;

const navStyle: React.CSSProperties = {
  display: "flex",
  justifyContent: "space-between",
  alignItems: "center",
  padding: "18px 40px",
  background: "white",
  borderBottom: "1px solid #e5e7eb",
  position: "sticky",
  top: 0,
  zIndex: 100,
};

const brandStyle: React.CSSProperties = {
  fontSize: "22px",
  fontWeight: "bold",
  textDecoration: "none",
  color: "#14b8a6",
};

const linksWrapperStyle: React.CSSProperties = {
  display: "flex",
  gap: "18px",
  alignItems: "center",
};

const linkStyle: React.CSSProperties = {
  textDecoration: "none",
  color: "#1f2937",
  fontWeight: 500,
};

const loginButtonStyle: React.CSSProperties = {
  border: "1px solid #14b8a6",
  color: "#14b8a6",
  padding: "8px 16px",
  borderRadius: "8px",
  textDecoration: "none",
  fontWeight: 500,
};

const registerButtonStyle: React.CSSProperties = {
  background: "#14b8a6",
  color: "white",
  padding: "8px 16px",
  borderRadius: "8px",
  textDecoration: "none",
  fontWeight: 500,
};

const logoutButtonStyle: React.CSSProperties = {
  background: "#ef4444",
  color: "white",
  border: "none",
  padding: "8px 16px",
  borderRadius: "8px",
  cursor: "pointer",
  fontWeight: 500,
};

function Navbar() {
  return (
    <nav style={navStyle}>
      <Link to="/" style={brandStyle}>
        TravelGraph
      </Link>

      <div style={linksWrapperStyle}>
        <Link to="/" style={linkStyle}>
          Home
        </Link>

        <Link to="/explore" style={linkStyle}>
          Explore
        </Link>

        <Link to="/planner" style={linkStyle}>
          Planner
        </Link>

        <Link to="/festivals" style={linkStyle}>
          Festivals
        </Link>

        {isLoggedIn ? (
          <>
            <Link to="/profile" style={linkStyle}>
              Profile
            </Link>

            <button style={logoutButtonStyle}>Logout</button>
          </>
        ) : (
          <>
            <Link to="/login" style={loginButtonStyle}>
              Login
            </Link>

            <Link to="/register" style={registerButtonStyle}>
              Register
            </Link>
          </>
        )}
      </div>
    </nav>
  );
}

export default Navbar;