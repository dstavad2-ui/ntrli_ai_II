# ============================================================================
# NTRLI' AI - AI/COMMERCIAL SEGREGATION ENFORCEMENT
# ============================================================================
"""
This module enforces strict segregation between AI and commercial operations.

CORE RULE: AI and commercial operations must be explicitly segregated.
AI cannot make decisions in transactional/commercial flows.

This ensures:
1. Customers receive deterministic, predictable service in commerce
2. AI is relegated to auxiliary functions (content, research, support)
3. No hallucination or drift in critical business operations
4. Clear legal/liability boundaries between AI and automation
"""

from typing import Literal, Set
from enum import Enum


class OperationType(Enum):
    """Classification of operation types."""

    # AI Operations - generative, non-deterministic, auxiliary
    AI_CONTENT_GENERATION = "ai_content_generation"  # Ad copy, descriptions
    AI_RESEARCH = "ai_research"  # Web research, information gathering
    AI_SUPPORT = "ai_support"  # Customer service responses
    AI_ANALYSIS = "ai_analysis"  # Data analysis, insights

    # Commercial Operations - deterministic, transactional, core business
    COMMERCIAL_ORDER = "commercial_order"  # Order processing
    COMMERCIAL_PAYMENT = "commercial_payment"  # Payment handling
    COMMERCIAL_INVENTORY = "commercial_inventory"  # Stock management
    COMMERCIAL_SHIPPING = "commercial_shipping"  # Fulfillment
    COMMERCIAL_PRICING = "commercial_pricing"  # Price calculations

    # Hybrid Operations - automation with optional AI assistance
    HYBRID_NOTIFICATION = "hybrid_notification"  # Notifications (templated)
    HYBRID_REPORTING = "hybrid_reporting"  # Reports (data + optional AI summary)


# AI operations - subject to 10 behavioral laws
AI_OPERATIONS: Set[OperationType] = {
    OperationType.AI_CONTENT_GENERATION,
    OperationType.AI_RESEARCH,
    OperationType.AI_SUPPORT,
    OperationType.AI_ANALYSIS,
}

# Commercial operations - pure automation, no AI decision-making allowed
COMMERCIAL_OPERATIONS: Set[OperationType] = {
    OperationType.COMMERCIAL_ORDER,
    OperationType.COMMERCIAL_PAYMENT,
    OperationType.COMMERCIAL_INVENTORY,
    OperationType.COMMERCIAL_SHIPPING,
    OperationType.COMMERCIAL_PRICING,
}

# Hybrid operations - automation with clearly bounded AI assistance
HYBRID_OPERATIONS: Set[OperationType] = {
    OperationType.HYBRID_NOTIFICATION,
    OperationType.HYBRID_REPORTING,
}


class SegregationViolation(RuntimeError):
    """Raised when AI/Commercial segregation is violated."""
    pass


class SegregationEnforcer:
    """
    Enforces AI/Commercial segregation.

    CORE RULE: AI operations and commercial operations must not mix.
    """

    @staticmethod
    def validate_operation(operation: OperationType, context: dict) -> None:
        """
        Validate that operation respects segregation boundaries.

        Args:
            operation: The type of operation being performed
            context: Operation context containing relevant data

        Raises:
            SegregationViolation: If segregation is violated
        """
        if operation in COMMERCIAL_OPERATIONS:
            # Commercial operations must be deterministic
            if context.get("uses_ai", False):
                raise SegregationViolation(
                    f"Commercial operation {operation.value} cannot use AI"
                )

            # Commercial operations must have validated inputs
            if not context.get("inputs_validated", False):
                raise SegregationViolation(
                    f"Commercial operation {operation.value} requires validated inputs"
                )

        elif operation in AI_OPERATIONS:
            # AI operations must follow 10 behavioral laws
            if not context.get("follows_10_laws", False):
                raise SegregationViolation(
                    f"AI operation {operation.value} must follow 10 behavioral laws"
                )

            # AI operations cannot be in critical path
            if context.get("is_critical_path", False):
                raise SegregationViolation(
                    f"AI operation {operation.value} cannot be in critical business path"
                )

        elif operation in HYBRID_OPERATIONS:
            # Hybrid operations must specify AI boundaries
            if context.get("uses_ai", False) and not context.get("ai_boundaries_defined", False):
                raise SegregationViolation(
                    f"Hybrid operation {operation.value} must define AI boundaries"
                )

    @staticmethod
    def is_ai_operation(operation: OperationType) -> bool:
        """Check if operation is AI-based."""
        return operation in AI_OPERATIONS

    @staticmethod
    def is_commercial_operation(operation: OperationType) -> bool:
        """Check if operation is commercial."""
        return operation in COMMERCIAL_OPERATIONS

    @staticmethod
    def is_hybrid_operation(operation: OperationType) -> bool:
        """Check if operation is hybrid."""
        return operation in HYBRID_OPERATIONS

    @staticmethod
    def get_segregation_report() -> dict:
        """
        Generate segregation boundary report.

        Returns:
            Dict containing current segregation configuration
        """
        return {
            "ai_operations": [op.value for op in AI_OPERATIONS],
            "commercial_operations": [op.value for op in COMMERCIAL_OPERATIONS],
            "hybrid_operations": [op.value for op in HYBRID_OPERATIONS],
            "segregation_enforced": True,
            "rule": "AI and commercial operations are strictly segregated"
        }


# ============================================================================
# TELEGRAM SHOP SPECIFIC BOUNDARIES
# ============================================================================

class TelegramShopBoundary:
    """
    Specific segregation rules for Telegram ecommerce shop.

    This defines exactly where AI is allowed and where it is prohibited.
    """

    # AI ALLOWED - Auxiliary functions
    AI_ALLOWED_CONTEXTS = {
        "product_description_generation",  # Generate product descriptions
        "marketing_content",  # Ad copy, promotional text
        "customer_inquiry_response",  # Support chat (non-transactional)
        "inventory_insights",  # Analysis and recommendations
    }

    # AI PROHIBITED - Core commerce functions
    AI_PROHIBITED_CONTEXTS = {
        "order_processing",  # Orders must be deterministic
        "payment_handling",  # Payments must be exact
        "price_calculation",  # Prices must be validated
        "inventory_updates",  # Stock must be accurate
        "shipping_confirmation",  # Fulfillment must be tracked
        "refund_processing",  # Financial ops must be exact
    }

    @staticmethod
    def validate_telegram_operation(context_name: str, uses_ai: bool) -> None:
        """
        Validate Telegram shop operation against boundaries.

        Args:
            context_name: Name of the operation context
            uses_ai: Whether AI is being used

        Raises:
            SegregationViolation: If AI used in prohibited context
        """
        if uses_ai and context_name in TelegramShopBoundary.AI_PROHIBITED_CONTEXTS:
            raise SegregationViolation(
                f"AI is prohibited in Telegram shop context: {context_name}. "
                f"This is a commercial operation requiring deterministic behavior."
            )

        if not uses_ai and context_name in TelegramShopBoundary.AI_ALLOWED_CONTEXTS:
            # This is fine - AI is optional in allowed contexts
            pass

    @staticmethod
    def get_boundaries() -> dict:
        """Get Telegram shop AI/commercial boundaries."""
        return {
            "ai_allowed": list(TelegramShopBoundary.AI_ALLOWED_CONTEXTS),
            "ai_prohibited": list(TelegramShopBoundary.AI_PROHIBITED_CONTEXTS),
            "enforcement": "strict",
            "rationale": "Customers expect deterministic outcomes in commerce"
        }
