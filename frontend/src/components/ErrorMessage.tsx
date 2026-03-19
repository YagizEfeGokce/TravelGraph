type ErrorMessageProps = {
  message: string;
};

function ErrorMessage({ message }: ErrorMessageProps) {
  return (
    <div
      style={{
        padding: "14px 16px",
        background: "#fef2f2",
        color: "#b91c1c",
        border: "1px solid #fecaca",
        borderRadius: "10px",
      }}
    >
      {message}
    </div>
  );
}

export default ErrorMessage;