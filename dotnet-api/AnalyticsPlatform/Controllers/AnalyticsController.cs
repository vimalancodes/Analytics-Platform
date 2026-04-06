using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using AnalyticsPlatform.Data;
using AnalyticsPlatform.Models;

namespace AnalyticsPlatform.Controllers
{
    [ApiController]
    [Route("api/[controller]")]
    public class AnalyticsController : ControllerBase
    {
        private readonly AnalyticsDbContext _db;
        private readonly ILogger<AnalyticsController> _logger;

        public AnalyticsController(AnalyticsDbContext db, ILogger<AnalyticsController> logger)
        {
            _db = db;
            _logger = logger;
        }

        // GET /api/analytics/summary
        [HttpGet("summary")]
        public async Task<IActionResult> GetSummary()
        {
            _logger.LogInformation("Fetching summary metrics");
            var metrics = await _db.SummaryMetrics
                .OrderByDescending(m => m.ComputedAt)
                .FirstOrDefaultAsync();

            if (metrics == null)
                return NotFound(new { message = "No summary metrics found. Run the pipeline first." });

            return Ok(metrics);
        }

        // GET /api/analytics/anomalies
        [HttpGet("anomalies")]
        public async Task<IActionResult> GetAnomalies()
        {
            _logger.LogInformation("Fetching anomalies");
            var anomalies = await _db.Anomalies
                .OrderByDescending(a => a.AnomalyScore)
                .ToListAsync();

            return Ok(new
            {
                total = anomalies.Count,
                data = anomalies
            });
        }

        // GET /api/analytics/invalid-records
        [HttpGet("invalid-records")]
        public async Task<IActionResult> GetInvalidRecords()
        {
            _logger.LogInformation("Fetching invalid records");
            var records = await _db.InvalidRecords
                .OrderByDescending(r => r.FlaggedAt)
                .ToListAsync();

            return Ok(new
            {
                total = records.Count,
                data = records
            });
        }

        // GET /api/analytics/insights
        [HttpGet("insights")]
        public async Task<IActionResult> GetInsights()
        {
            _logger.LogInformation("Fetching AI insights");
            var insights = await _db.AiInsights
                .OrderByDescending(i => i.GeneratedAt)
                .ToListAsync();

            return Ok(new
            {
                total = insights.Count,
                data = insights
            });
        }

        // GET /api/analytics/valid-records
        [HttpGet("valid-records")]
        public async Task<IActionResult> GetValidRecords()
        {
            _logger.LogInformation("Fetching valid records");
            var records = await _db.ValidRecords
                .OrderByDescending(r => r.ProcessedAt)
                .ToListAsync();

            return Ok(new
            {
                total = records.Count,
                data = records
            });
        }

        // GET /api/analytics/revenue-by-region
        [HttpGet("revenue-by-region")]
        public async Task<IActionResult> GetRevenueByRegion()
        {
            _logger.LogInformation("Fetching revenue by region");
            var result = await _db.ValidRecords
                .GroupBy(r => r.Region)
                .Select(g => new
                {
                    region = g.Key,
                    totalOrders = g.Count(),
                    totalRevenue = g.Sum(r => r.TotalAmount),
                    avgOrderValue = g.Average(r => r.TotalAmount)
                })
                .OrderByDescending(r => r.totalRevenue)
                .ToListAsync();

            return Ok(result);
        }

        // GET /api/analytics/revenue-by-category
        [HttpGet("revenue-by-category")]
        public async Task<IActionResult> GetRevenueByCategory()
        {
            _logger.LogInformation("Fetching revenue by category");
            var result = await _db.ValidRecords
                .GroupBy(r => r.Category)
                .Select(g => new
                {
                    category = g.Key,
                    totalOrders = g.Count(),
                    totalRevenue = g.Sum(r => r.TotalAmount),
                    avgOrderValue = g.Average(r => r.TotalAmount)
                })
                .OrderByDescending(r => r.totalRevenue)
                .ToListAsync();

            return Ok(result);
        }

        // POST /api/analytics/process
        [HttpPost("process")]
        public IActionResult ProcessData()
        {
            _logger.LogInformation("Process data endpoint triggered");
            return Ok(new
            {
                message = "Pipeline is managed via Python. Run: python main.py in the python-pipeline folder.",
                status = "info",
                timestamp = DateTime.UtcNow
            });
        }
    }
}