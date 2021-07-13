from datetime import datetime


class CustomAssertions:
    def assertObject(self, actual, expected):
        """Assert that a model is equivalent to its dict counterpart.

        Verifies that all properties have been set correctly
        Verifies that all set properties can be accessed by dot notation
        """
        # if actual and expected are the same type, just compare with ==
        if type(actual) == type(expected):
            if actual != expected:
                raise AssertionError(
                    "actual did not match expected value:\nexpected: {0}\nactual: {1}".format(
                        expected, actual
                    )
                )
            return

        if isinstance(actual, datetime):
            if actual.microsecond:
                actual = datetime.strftime(actual, "%Y-%m-%dT%H:%M:%S.%fZ")
            else:
                actual = datetime.strftime(actual, "%Y-%m-%dT%H:%M:%SZ")
            if actual != expected:
                raise AssertionError(
                    "actual did not match expected value:\nexpected: {0}\nactual: {1}".format(
                        expected, actual
                    )
                )
            return

        # if we get here, actual is an model class object so do the complicated logic
        for key, value in expected.items():
            actual_value = getattr(actual, key)

            if type(value) is list:
                if len(value) != len(actual_value):
                    raise AssertionError(
                        "actual.{0} did not match expected value:\nexpected: {1} - length: {2}\nactual: {3} - length: {4}".format(
                            key, value, len(value), actual_value, len(actual_value)
                        )
                    )

                for i in range(len(value)):
                    self.assertObject(actual_value[i], value[i])

            else:
                self.assertObject(actual_value, value)
