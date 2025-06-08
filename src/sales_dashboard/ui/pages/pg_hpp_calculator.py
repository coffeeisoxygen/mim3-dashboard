# """HPP Calculator - Dynamic cost/margin with subsidy calculation."""

# from __future__ import annotations

# import streamlit as st

# from sales_dashboard.core.streamlit_session_manager import PageName, session_manager
# from sales_dashboard.ui.ui_config import ICONS


# def show_hpp_calculator_page() -> None:
#     """Main HPP Calculator with dynamic cost/margin interface."""
#     # 🔐 AUTH CHECK - This was missing!
#     user = session_manager.require_page_access(PageName.HPP_CALCULATOR)

#     st.markdown("## 📊 HPP Calculator")
#     st.markdown(
#         "Calculate unit pricing with dynamic cost, margin, and subsidy analysis"
#     )

#     # Create tabs for different calculation types
#     tab_rgu, tab_trade = st.tabs([
#         f"{ICONS.DASHBOARD} RGU Analysis",
#         "💰 Trade Analysis",
#     ])

#     with tab_rgu:
#         _render_dynamic_hpp_calculator()

#     with tab_trade:
#         _render_trade_calculator()


# def _render_dynamic_hpp_calculator() -> None:
#     """Dynamic HPP calculator with cost/margin sides."""
#     st.markdown("### Dynamic Cost & Margin Analysis")

#     # Initialize session state for dynamic parameters
#     if "cost_items" not in st.session_state:
#         st.session_state.cost_items = [
#             {"name": "SP_KIT", "value": 10000.0, "quantity": 450},
#             {"name": "RELOAD", "value": 20000.0, "quantity": 450},
#         ]

#     if "margin_items" not in st.session_state:
#         st.session_state.margin_items = [
#             {"name": "ACQ Revenue", "percentage": 15.0, "multiplier": 0.0},
#             {"name": "Up Front Disc", "percentage": 1.5, "multiplier": 0.0},
#             {
#                 "name": "Trade Inner",
#                 "percentage": 2.0,
#                 "multiplier": 9000000.0,
#             },  # Your example
#             {"name": "Tertiary Inner", "percentage": 2.0, "multiplier": 0.0},
#         ]

#     # Two-column layout: Cost vs Margin
#     col_cost, col_margin = st.columns(2)

#     with col_cost:
#         _render_cost_section()

#     with col_margin:
#         _render_margin_section()

#     # Calculate button
#     st.markdown("---")
#     if st.button("🧮 Calculate Totals", type="primary", use_container_width=True):
#         total_cost, total_margin = _calculate_totals()
#         _render_hpp_calculation(total_cost, total_margin)


# def _render_cost_section() -> None:
#     """Render dynamic cost input section."""
#     st.markdown("### 💰 Cost Components")

#     # Add/Clear controls
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("➕ Add Cost", key="add_cost"):
#             st.session_state.cost_items.append({
#                 "name": f"Cost Item {len(st.session_state.cost_items) + 1}",
#                 "value": 0.0,
#                 "quantity": 1,
#             })
#             st.rerun()

#     with col2:
#         if st.button("🗑️ Clear All", key="clear_costs"):
#             st.session_state.cost_items = []
#             st.rerun()

#     # Dynamic cost items
#     for i, item in enumerate(st.session_state.cost_items):
#         with st.container():
#             st.markdown(f"**Cost Item {i + 1}**")

#             col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

#             with col1:
#                 item["name"] = st.text_input(
#                     "Name",
#                     value=item["name"],
#                     key=f"cost_name_{i}",
#                     label_visibility="collapsed",
#                 )

#             with col2:
#                 item["value"] = st.number_input(
#                     "Unit Cost",
#                     value=item["value"],
#                     min_value=0.0,
#                     format="%.0f",
#                     key=f"cost_value_{i}",
#                     label_visibility="collapsed",
#                 )

#             with col3:
#                 item["quantity"] = st.number_input(
#                     "Qty",
#                     value=item["quantity"],
#                     min_value=1,
#                     key=f"cost_qty_{i}",
#                     label_visibility="collapsed",
#                 )

#             with col4:
#                 if st.button("🗑️", key=f"del_cost_{i}", help="Delete this item"):
#                     st.session_state.cost_items.pop(i)
#                     st.rerun()

#             # Show subtotal
#             subtotal = item["value"] * item["quantity"]
#             st.caption(f"Subtotal: Rp {subtotal:,.0f}")

#         st.markdown("")


# def _render_margin_section() -> None:
#     """Render dynamic margin input section with percentage × multiplier logic."""
#     st.markdown("### 📈 Margin Components")

#     # Add/Clear controls
#     col1, col2 = st.columns(2)
#     with col1:
#         if st.button("➕ Add Margin", key="add_margin"):
#             st.session_state.margin_items.append({
#                 "name": f"Margin Item {len(st.session_state.margin_items) + 1}",
#                 "percentage": 0.0,
#                 "multiplier": 0.0,
#             })
#             st.rerun()

#     with col2:
#         if st.button("🗑️ Clear All", key="clear_margins"):
#             st.session_state.margin_items = []
#             st.rerun()

#     # Column headers for clarity
#     st.markdown("**Name | Percentage | Multiplier | Action**")

#     # Dynamic margin items
#     for i, item in enumerate(st.session_state.margin_items):
#         with st.container():
#             st.markdown(f"**Margin Item {i + 1}**")

#             col1, col2, col3, col4 = st.columns([2, 1, 2, 1])

#             with col1:
#                 item["name"] = st.text_input(
#                     "Name",
#                     value=item["name"],
#                     key=f"margin_name_{i}",
#                     label_visibility="collapsed",
#                     placeholder="e.g., Trade Inner",
#                 )

#             with col2:
#                 item["percentage"] = st.number_input(
#                     "Percentage",
#                     value=item["percentage"],
#                     min_value=0.0,
#                     max_value=100.0,
#                     format="%.2f",
#                     key=f"margin_percentage_{i}",
#                     label_visibility="collapsed",
#                     help="Percentage rate (e.g., 2.0 for 2%)",
#                 )

#             with col3:
#                 item["multiplier"] = st.number_input(
#                     "Multiplier",
#                     value=item["multiplier"],
#                     min_value=0.0,
#                     format="%.0f",
#                     key=f"margin_multiplier_{i}",
#                     label_visibility="collapsed",
#                     help="Amount to multiply percentage with (e.g., total inject reload)",
#                 )

#             with col4:
#                 if st.button("🗑️", key=f"del_margin_{i}", help="Delete this item"):
#                     st.session_state.margin_items.pop(i)
#                     st.rerun()

#             # Show calculated margin with clear formula
#             if item["multiplier"] > 0 and item["percentage"] > 0:
#                 margin_value = item["multiplier"] * (item["percentage"] / 100)
#                 st.caption(
#                     f"💰 {item['percentage']}% × Rp {item['multiplier']:,.0f} = Rp {margin_value:,.0f}"
#                 )
#             else:
#                 st.caption("ℹ️ Set percentage and multiplier to calculate")

#         st.markdown("")


# def _calculate_totals() -> tuple[float, float]:
#     """Calculate total cost and total margin with fixed logic."""
#     # Calculate total cost (unchanged)
#     total_cost = sum(
#         item["value"] * item["quantity"] for item in st.session_state.cost_items
#     )

#     # Calculate total margin with percentage × multiplier logic
#     total_margin = sum(
#         item["multiplier"] * (item["percentage"] / 100)
#         for item in st.session_state.margin_items
#         if item["multiplier"] > 0 and item["percentage"] > 0
#     )

#     return total_cost, total_margin


# def _render_hpp_calculation(total_cost: float, total_margin: float) -> None:
#     """Render HPP calculation with subsidy input."""
#     st.markdown("---")
#     st.markdown("### 🎯 HPP Calculation")

#     # Display totals
#     col1, col2, col3 = st.columns(3)

#     with col1:
#         st.metric("Total Cost", f"Rp {total_cost:,.0f}")

#     with col2:
#         st.metric("Total Margin", f"Rp {total_margin:,.0f}")

#     with col3:
#         net_available = total_margin - total_cost if total_margin > total_cost else 0
#         st.metric("Available for Subsidy", f"Rp {net_available:,.0f}")

#     # Subsidy and quantity inputs
#     st.markdown("**HPP Configuration**")
#     col1, col2 = st.columns(2)

#     with col1:
#         subsidy_amount = st.number_input(
#             "Subsidy from Margin",
#             min_value=0.0,
#             max_value=total_margin,
#             value=min(total_margin, total_cost / 2),  # Default to reasonable subsidy
#             format="%.0f",
#             help="How much margin to use as subsidy",
#         )

#     with col2:
#         total_pieces = st.number_input(
#             "Total Pieces", min_value=1, value=20, help="Number of units to produce"
#         )

#     # Calculate HPP
#     if total_pieces > 0:
#         effective_cost = total_cost - subsidy_amount
#         hpp_per_piece = effective_cost / total_pieces
#         remaining_margin = total_margin - subsidy_amount

#         # Display results
#         st.markdown("**📊 Final Results**")
#         col1, col2, col3 = st.columns(3)

#         with col1:
#             st.metric(
#                 "HPP per Piece",
#                 f"Rp {hpp_per_piece:,.0f}",
#                 help="Final unit price after subsidy",
#             )

#         with col2:
#             st.metric(
#                 "Effective Cost",
#                 f"Rp {effective_cost:,.0f}",
#                 delta=f"-Rp {subsidy_amount:,.0f} subsidy",
#                 delta_color="normal",
#             )

#         with col3:
#             st.metric(
#                 "Remaining Margin",
#                 f"Rp {remaining_margin:,.0f}",
#                 help="Margin left after subsidy",
#             )


# def _render_trade_calculator() -> None:
#     """Trade (Saldo) focused calculation - placeholder."""
#     st.markdown("### Trade (Saldo) Analysis")
#     st.info("🚧 Trade calculation will be implemented with similar dynamic structure.")

#     st.markdown("**Will include:**")
#     st.markdown("- Dynamic trade cost components")
#     st.markdown("- Dynamic saldo margin streams")
#     st.markdown("- Subsidy calculation for trade pricing")
