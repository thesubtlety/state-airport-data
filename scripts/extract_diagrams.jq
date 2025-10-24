[
  .digital_tpp.state_code[]?
  | .city_name
  | if type == "array" then .[] else . end
  | select(type == "object")
  | .airport_name // empty
  | if type == "array" then .[] else . end
  | select(type == "object")
  | select(.record != null)
  | select(
      .record
      | if type == "array" then
          any(.chart_name == "AIRPORT DIAGRAM")
        else
          .chart_name == "AIRPORT DIAGRAM"
        end
    )
  | {
      key: (."+@apt_ident"),
      value: (
        [.record | if type == "array" then .[] else . end | select(.chart_name == "AIRPORT DIAGRAM") | .pdf_name]
        | first
      )
    }
]
| from_entries
