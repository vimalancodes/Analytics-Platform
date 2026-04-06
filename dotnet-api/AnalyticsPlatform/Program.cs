using Microsoft.EntityFrameworkCore;
using AnalyticsPlatform.Data;
using Serilog;

Log.Logger = new LoggerConfiguration()
    .WriteTo.Console()
    .CreateLogger();

var builder = WebApplication.CreateBuilder(args);

builder.Host.UseSerilog();

var connectionString = builder.Configuration.GetConnectionString("DefaultConnection")
    ?? "Host=localhost;Port=5432;Database=analytics_db;Username=analytics_user;Password=analytics_pass";

builder.Services.AddDbContext<AnalyticsDbContext>(options =>
    options.UseNpgsql(connectionString));

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();

var app = builder.Build();

app.UseHttpsRedirection();
app.MapControllers();

app.MapGet("/", () => new
{
    message = "Analytics Platform API",
    version = "1.0",
    endpoints = new[]
    {
        "GET  /api/analytics/summary",
        "GET  /api/analytics/anomalies",
        "GET  /api/analytics/invalid-records",
        "GET  /api/analytics/insights",
        "GET  /api/analytics/valid-records",
        "GET  /api/analytics/revenue-by-region",
        "GET  /api/analytics/revenue-by-category",
        "POST /api/analytics/process"
    }
});

app.Run();