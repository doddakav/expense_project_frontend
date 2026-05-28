import streamlit as st
import requests
import pandas as pd

server_loc = st.secrets["server_url"]

st.title("Expense Tracker")

if "name" not in st.session_state:
    st.session_state.name = ""

if "amount" not in st.session_state:
    st.session_state.amount = 0.0

if "category" not in st.session_state:
    st.session_state.category = ""

if "expense_date" not in st.session_state:
    st.session_state.expense_date = ""


opt = st.sidebar.selectbox(
    "choose a option",
    [
        "Add expenses",
        "View expenses",
        "Update expenses",
        "Delete expenses",
        "Search expenses",
        "Sort Expenses"
    ]
)

if opt == "Add expenses":

    st.header("Add Expenses")

    with st.form("Adding_Expenses"):

        name = st.text_input("Expense Name")

        amount = st.number_input(
            "amount",
            min_value=0.0
        )

        category = st.selectbox(
            "choose type of expense",
            [
                "Food",
                "Travel",
                "Shopping",
                "Bills",
                "Health",
                "Other"
            ]
        )

        date = st.date_input("Expense_date")

        if st.form_submit_button("Add Expense"):

            expense = {
                "name": name,
                "amount": amount,
                "category": category,
                "date": str(date)
            }

            try:

                res = requests.post(
                    f"{server_loc}/add_expense",
                    json=expense
                )

                st.write(res.json())

            except Exception as e:

                st.error(e)



elif opt == "View expenses":

    st.header("View expenses")

    btn = st.button("View Expenses")

    if btn:

        try:

            res = requests.get(
                f"{server_loc}/View_expenses"
            )

            all_exp = res.json()

            if "all_expenses" in all_exp:

                exp = all_exp["all_expenses"]

                pd_df = pd.DataFrame(exp)

                st.dataframe(pd_df)

            else:

                st.error(all_exp)

        except Exception as e:

            st.error(e)


elif opt == "Update expenses":

    st.header("Update expenses")

    exp_to_update = st.number_input(
        "enter expense id",
        min_value=1
    )

    btn = st.button("Show expenses")

    if btn:

        try:

            res = requests.get(
                f"{server_loc}/get_single_expense/{exp_to_update}"
            )

            data = res.json()

            st.write(data)

            if (
                res.status_code == 200
                and data["exp_data"] is not None
            ):

                st.session_state.name = data["exp_data"]["name"]

                st.session_state.amount = data["exp_data"]["amount"]

                st.session_state.category = data["exp_data"]["category"]

                st.session_state.expense_date = data["exp_data"]["expense_date"]

            else:

                st.error("Expense not found")

        except Exception as e:

            st.error(e)



    name = st.text_input(
        "name",
        value=st.session_state.name
    )

    amount = st.number_input(
        "amount",
        value=float(st.session_state.amount)
    )

    category = st.text_input(
        "category",
        value=st.session_state.category
    )

    expense_date = st.text_input(
        "Date",
        value=str(st.session_state.expense_date)
    )


    if st.button("update expense"):

        try:

            update_expense = {
                "name": name,
                "amount": amount,
                "category": category,
                "date": expense_date
            }

            res = requests.put(
                f"{server_loc}/update_expense/{exp_to_update}",
                json=update_expense
            )

            if res.status_code == 200:

                st.success(
                    res.json()["update"]
                )

            else:

                st.error(res.text)

        except Exception as e:

            st.error(e)

elif opt == "Delete expenses":

    st.header("Delete expense")

    try:

        res = requests.get(
            f"{server_loc}/View_expenses"
        )

        all_exp = res.json()

        if "all_expenses" in all_exp:

            exp = all_exp["all_expenses"]

            pd_df = pd.DataFrame(exp)

            st.dataframe(pd_df)

    except Exception as e:

        st.error(e)


    exp_id_delete = st.number_input(
        "expense to delete",
        min_value=1,
        step=1
    )

    if st.button("Delete"):

        try:

            res = requests.delete(
                f"{server_loc}/delete_expenses/{exp_id_delete}"
            )

            if res.status_code == 200:

                st.success(
                    res.json()["deleted"]
                )

            else:

                st.error(res.text)

        except Exception as e:

            st.error(e)

elif opt == "Search expenses":

    st.header("Search expenses")

    search_category = st.text_input(
        "Search Category"
    )

    if st.button("Search"):

        try:

            res = requests.get(
                f"{server_loc}/search_category/{search_category}"
            )

            if res.status_code == 200:

                data = res.json()["search"]

                pd_df = pd.DataFrame(data)

                st.dataframe(pd_df)

            else:

                st.error(res.text)

        except Exception as e:

            st.error(e)

elif opt == "Sort Expenses":

    st.header("Sort Expenses")

    sort_type = st.selectbox(
        "choose sorting",
        [
            "date descending",
            "date ascending",
            "lowest amount",
            "highest amount"
        ]
    )

    if st.button("Sort"):

        try:

            res = requests.get(
                f"{server_loc}/sort_by/{sort_type}"
            )

            if res.status_code == 200:

                data = res.json()["sorted"]

                pd_df = pd.DataFrame(data)

                st.dataframe(pd_df)

            else:

                st.error(res.text)

        except Exception as e:

            st.error(e)