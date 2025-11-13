# Kimi AI Chat App - Deployment Guide

## Quick Start

### Option 1: Run Directly (Recommended for Testing)

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application**:
   ```bash
   streamlit run kimi_chat_app.py
   ```

3. **Open your browser** and go to `http://localhost:8501`

### Option 2: Use Run Scripts

**Windows**:
```bash
run_app.bat
```

**Linux/Mac**:
```bash
./run_app.sh
```

## Pre-Deployment Checklist

- [ ] Get Kimi AI API key from [platform.moonshot.cn](https://platform.moonshot.cn)
- [ ] Add credits to your account (minimum $1 recommended)
- [ ] Install Python 3.8 or higher
- [ ] Install required dependencies
- [ ] Test API connection using `test_kimi_api.py`

## Testing Your Setup

Before running the main app, test your API connection:

```bash
python test_kimi_api.py
```

This will verify:
- API key validity
- Network connectivity
- Basic chat functionality
- Available models

## Configuration

### Required Environment Variables

For production deployment, set these environment variables:

```bash
export KIMI_API_KEY="your_api_key_here"
```

### Model Options

The app supports these Kimi AI models:
- `kimi-k2-turbo-preview` (fastest, recommended)
- `kimi-k2-0711-preview` (latest stable)
- `kimi-k2-0905-preview` (enhanced reasoning)
- `moonshot-v1-8k` (standard context)
- `moonshot-v1-32k` (extended context)
- `moonshot-v1-128k` (maximum context)

## Deployment Options

### 1. Local Development
```bash
streamlit run kimi_chat_app.py --server.port=8501 --server.address=localhost
```

### 2. Streamlit Cloud
1. Push code to GitHub
2. Connect to [share.streamlit.io](https://share.streamlit.io)
3. Deploy from repository

### 3. Docker Deployment
Create a `Dockerfile`:
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "kimi_chat_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 4. Cloud Platforms
- **AWS**: Use EC2 or AWS Fargate
- **Google Cloud**: App Engine or Cloud Run
- **Azure**: App Service or Container Instances

## Security Best Practices

1. **API Key Management**:
   - Never commit API keys to version control
   - Use environment variables in production
   - Rotate keys regularly

2. **Network Security**:
   - Use HTTPS in production
   - Configure firewall rules
   - Monitor API usage

3. **Access Control**:
   - Implement user authentication if needed
   - Rate limiting for public deployments
   - Monitor for abuse

## Troubleshooting

### Common Issues

1. **API Key Issues**:
   - Verify key is correct and active
   - Check account has sufficient credits
   - Ensure key has proper permissions

2. **Connection Problems**:
   - Check internet connectivity
   - Verify firewall settings
   - Test with `curl` to API endpoint

3. **Performance Issues**:
   - Choose appropriate model for your needs
   - Adjust temperature and token limits
   - Monitor API rate limits

### Debug Commands

```bash
# Test API connectivity
curl -H "Authorization: Bearer YOUR_API_KEY" https://api.moonshot.cn/v1/models

# Check Python environment
python --version
pip list | grep -E "(streamlit|openai)"

# Run with debug logging
streamlit run kimi_chat_app.py --logger.level=debug
```

## Monitoring & Maintenance

### Health Checks
- Monitor API response times
- Track error rates
- Check API usage quotas

### Updates
- Keep dependencies updated
- Monitor Kimi AI API changes
- Update models when new versions available

## Support

- **Kimi AI Documentation**: [platform.moonshot.cn/docs](https://platform.moonshot.cn/docs)
- **Streamlit Documentation**: [docs.streamlit.io](https://docs.streamlit.io)
- **API Issues**: Check Moonshot AI status page

## Next Steps

After successful deployment:
1. Customize the UI for your brand
2. Add user management features
3. Implement conversation history storage
4. Add analytics and monitoring
5. Consider adding voice input/output capabilities

---

**Good luck with your Kimi AI Chat App! 🤖✨**