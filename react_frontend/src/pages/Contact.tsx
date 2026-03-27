export default function Contact() {
  return (
    <div className="container py-12">
      <div
        className="mx-auto max-w-2xl rounded-2xl border bg-card p-8 text-center"
        style={{ boxShadow: "var(--shadow-card)" }}
      >
        <h1 className="mb-3 font-display text-3xl font-bold text-foreground">Contact</h1>
        <p className="text-lg font-semibold text-primary">Anushka Singh</p>
        <a
          href="mailto:anushka.singh2319@gmail.com"
          className="mt-2 inline-block text-muted-foreground underline decoration-primary/40 underline-offset-4 hover:text-foreground"
        >
          anushka.singh2319@gmail.com
        </a>
      </div>
    </div>
  );
}
