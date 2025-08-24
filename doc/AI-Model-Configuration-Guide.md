# AI Model Configuration Guide
## Malaysian Business Intelligence Call Center System

### Quick Model Switching

Your system is now fully configurable! To change AI models, simply update your `.env` file:

```bash
# Copy .env.template to .env first (if not done already)
cp .env.template .env

# Edit your .env file with your preferred model
OPENAI_MODEL=your_preferred_model
OPENAI_MAX_TOKENS=token_limit
OPENAI_TEMPERATURE=creativity_level
```

### Model Options & Recommendations for Malaysian Business Context

#### 🏆 **GPT-4 (Current - Premium Choice)**
```bash
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2500
OPENAI_TEMPERATURE=0.3
```
- **Best for:** Complex Malaysian business analysis, cultural nuances, RM financial calculations
- **Cost:** ~$0.03/1K input tokens, $0.06/1K output tokens
- **Strengths:** Superior reasoning, cultural context understanding, mathematical precision
- **Use when:** Budget allows, need highest quality insights

#### 💡 **GPT-4-Turbo (Balanced Choice)**
```bash
OPENAI_MODEL=gpt-4-turbo
OPENAI_MAX_TOKENS=2500
OPENAI_TEMPERATURE=0.3
```
- **Best for:** High-quality analysis at lower cost
- **Cost:** ~60% less than GPT-4
- **Strengths:** Faster responses, good Malaysian context understanding
- **Use when:** Need quality with cost optimization

#### 💰 **GPT-3.5-Turbo (Cost-Effective)**
```bash
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=2000  # Reduced for simpler analysis
OPENAI_TEMPERATURE=0.2  # Lower for consistency
```
- **Best for:** Basic insights, trend analysis, simple recommendations
- **Cost:** ~95% cheaper than GPT-4
- **Strengths:** Very fast, handles Malaysian currency/dates well
- **Use when:** High volume analysis, budget constraints, basic insights sufficient

#### 🚀 **GPT-4o (Latest - If Available)**
```bash
OPENAI_MODEL=gpt-4o
OPENAI_MAX_TOKENS=2500
OPENAI_TEMPERATURE=0.3
```
- **Best for:** Latest capabilities, potential multimodal features
- **Cost:** Similar to GPT-4
- **Use when:** Want cutting-edge capabilities

### Malaysian Business Context Performance

| Model | Malaysian Context | RM Calculations | Cultural Insights | Festival Awareness | Cost |
|-------|------------------|-----------------|-------------------|-------------------|------|
| GPT-4 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 💰💰💰 |
| GPT-4-Turbo | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 💰💰 |
| GPT-3.5-Turbo | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | 💰 |

### Token Recommendations by Model

**For Malaysian Business Analysis:**
- **GPT-4/GPT-4-Turbo:** 2500 tokens (comprehensive analysis)
- **GPT-3.5-Turbo:** 2000 tokens (focused analysis)
- **Simple Insights:** 1500 tokens (basic recommendations)

### Temperature Settings Guide

```bash
# Conservative (Consistent, Factual)
OPENAI_TEMPERATURE=0.1  # Most consistent RM calculations

# Balanced (Current Setting)
OPENAI_TEMPERATURE=0.3  # Good mix of accuracy & creativity

# Creative (More varied insights)
OPENAI_TEMPERATURE=0.5  # More diverse business recommendations
```

### Cost Optimization Strategies

#### 1. **Hybrid Approach** (Recommended)
- Use **GPT-4** for complex analysis (Executive Dashboard)
- Use **GPT-3.5-Turbo** for operational metrics
- Switch via environment variables based on dashboard type

#### 2. **Time-Based Switching**
- **Peak hours:** GPT-3.5-Turbo (fast responses)
- **Detailed reports:** GPT-4 (comprehensive analysis)

#### 3. **Volume-Based**
- **High-frequency updates:** GPT-3.5-Turbo
- **Strategic insights:** GPT-4

### Implementation Examples

#### Switching to Cost-Effective Mode:
```bash
# In your .env file
OPENAI_MODEL=gpt-3.5-turbo
OPENAI_MAX_TOKENS=2000
OPENAI_TEMPERATURE=0.2

# Restart your application
./start-callcenter.sh
```

#### Premium Analysis Mode:
```bash
# In your .env file
OPENAI_MODEL=gpt-4
OPENAI_MAX_TOKENS=2500
OPENAI_TEMPERATURE=0.3

# Restart your application
./start-callcenter.sh
```

### Testing Different Models

1. **Backup your current .env:**
   ```bash
   cp .env .env.backup
   ```

2. **Test GPT-3.5-Turbo:**
   ```bash
   # Update .env with GPT-3.5 settings
   # Restart app and compare insights quality
   ```

3. **Compare outputs** for your Malaysian business context
4. **Choose based on** quality vs. cost requirements

### Monitoring Model Performance

The system will work seamlessly with any supported OpenAI model. Monitor:
- **Response quality** for Malaysian business insights
- **RM calculation accuracy** 
- **Cultural context relevance**
- **Cost per analysis session**

### Future Model Support

Your system is ready for future OpenAI models:
- Simply update `OPENAI_MODEL` in your `.env`
- The Malaysian business prompts will work with newer models
- Token limits may need adjustment for future models

---

**Ready to switch models?** Just update your `.env` file and restart the application!
