# AI Customer Support Observability System

## Overview

This project demonstrates how I would monitor and debug an AI customer-support application after it is deployed to production.

The main idea is simple:

> When an AI application becomes slow, gives a wrong answer, becomes expensive, or crashes, we need evidence to find the actual problem instead of guessing.

The system provides a FastAPI backend and a simple frontend with request tracing, logging, processing-time measurement, error handling, rate limiting, health checks, and application metrics.

---
# Problem Statement

The StackLab scenario describes an AI customer-support application:

```text
React Frontend
      ↓
FastAPI Backend
      ↓
RAG System
      ↓
Vector Database
      ↓
LLM API
      ↓
MySQL
