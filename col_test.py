    def column_value_difference(
            self,
            other: "LegacyApiTdsFrame",
            self_join_columns: PyLegendList[str],
            other_join_columns: PyLegendList[str],
            columns_to_check: PyLegendList[str]
    ) -> "LegacyApiTdsFrame":
        from pylegend.core.tds.legacy_api.frames.legacy_api_applied_function_tds_frame import (
            LegacyApiAppliedFunctionTdsFrame
        )
        from pylegend.core.tds.legacy_api.frames.functions.legacy_api_column_value_difference_function import (
            LegacyApiColumnValueDifferenceFunction
        )
        return LegacyApiAppliedFunctionTdsFrame(
            LegacyApiColumnValueDifferenceFunction(
                self, other, self_join_columns, other_join_columns, columns_to_check
            )
        )

        with pytest.raises(TypeError, match="columns_to_check parameter must be a list of strings."):
            frame1.column_value_difference(frame2, ["id"], ["id"], 'val')  # type: ignore

    def test_column_value_difference_validation_checks(self) -> None:
        cols1 = [
            PrimitiveTdsColumn.integer_column("id"),
            PrimitiveTdsColumn.integer_column("key"),
            PrimitiveTdsColumn.integer_column("val"),
        ]
        frame1: LegacyApiTdsFrame = LegacyApiTableSpecInputFrame(['test_schema', 'test_table1'], cols1)

        cols2 = [
            PrimitiveTdsColumn.integer_column("id"),
            PrimitiveTdsColumn.integer_column("val"),
        ]
        frame2: LegacyApiTdsFrame = LegacyApiTableSpecInputFrame(['test_schema', 'test_table2'], cols2)

        # Join column list length mismatch
        with pytest.raises(ValueError, match="self_join_columns and other_join_columns should be of the same size"):
            frame1.column_value_difference(frame2, ["id", "key"], ["id"], ["val"])

        # Self join column not found
        with pytest.raises(RuntimeError, match="Join column: 'missing' not found in self"):
            frame1.column_value_difference(frame2, ["missing"], ["id"], ["val"])

        # Other join column not found
        with pytest.raises(RuntimeError, match="Join column: 'missing' not found in other"):
            frame1.column_value_difference(frame2, ["id"], ["missing"], ["val"])

        # Difference column not found in self
        cols2_extra = [
            PrimitiveTdsColumn.integer_column("id"),
            PrimitiveTdsColumn.integer_column("val"),
            PrimitiveTdsColumn.integer_column("extra"),
        ]
        frame2_extra: LegacyApiTdsFrame = LegacyApiTableSpecInputFrame(['test_schema', 'test_table2'], cols2_extra)
        with pytest.raises(RuntimeError, match="Difference column: 'extra' not found in self"):
            frame1.column_value_difference(frame2_extra, ["id"], ["id"], ["extra"])

        # Difference column not found in other
        with pytest.raises(RuntimeError, match="Difference column: 'key' not found in other"):
            frame1.column_value_difference(frame2, ["id"], ["id"], ["key"])

        # Duplicate final column names
        cols_dup1 = [
            PrimitiveTdsColumn.integer_column("val_1"),
            PrimitiveTdsColumn.integer_column("val"),
        ]
        frame_dup1: LegacyApiTdsFrame = LegacyApiTableSpecInputFrame(['test_schema', 'test_table1'], cols_dup1)
        cols_dup2 = [
            PrimitiveTdsColumn.integer_column("val_1"),
            PrimitiveTdsColumn.integer_column("val"),
        ]
        frame_dup2: LegacyApiTdsFrame = LegacyApiTableSpecInputFrame(['test_schema', 'test_table2'], cols_dup2)
        with pytest.raises(RuntimeError, match="Duplicate column names in column difference not supported"):
            frame_dup1.column_value_difference(frame_dup2, ["val_1"], ["val_1"], ["val"])
